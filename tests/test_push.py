from .conftest import *

WRITE_URL = None
WRITE_BUCKET = os.environ.get("WRITE_BUCKET")
TIMESTAMP = int(round(time.time()))
WRITE_URL = f"quilt+s3://{WRITE_BUCKET}#package=test/{TIMESTAMP}"

logging.info(f"WRITE_BUCKET: [{WRITE_BUCKET}]")
if not WRITE_BUCKET:
    pytest.skip("no writeable bucket available", allow_module_level=True)


@pytest.fixture
def pkg():
    return QuiltPackage.FromURI(WRITE_URL)


async def test_push(pkg: QuiltPackage):
    print(WRITE_URL)
    assert pkg is not None

    # Create new Package
    pkg.write_text(f"# Hello World!\n{TIMESTAMP}", "README.md")
    qpkg = await pkg.put("README")
    assert qpkg is not None

    # Read that Package
    files = await pkg.list()
    assert "README.md" in files

    # Add a file
    pkg.write_text(f"# Goodbye Cruel World!\n{TIMESTAMP}", "WRITEME.md")

    # Verify diff
    diffs = await pkg.diff()
    assert "WRITEME.md" in diffs["added"]

    # Update Package
    qpkg2 = await pkg.post("WRITEME")
    assert qpkg2 is not None

    # Verify Result using legacy quilt3 APIs
    q3 = Package.browse(pkg.name, pkg.registry)
    files3 = list(q3.keys())
    assert "README.md" in files3
    assert "WRITEME.md" in files3
