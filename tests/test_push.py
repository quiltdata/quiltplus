from .conftest import *

TIMESTAMP = QuiltConfig.Now()
WRITE_URL = None
WRITE_BUCKET = os.environ.get("WRITE_BUCKET")
WRITE_URL = f"quilt+s3://{WRITE_BUCKET}#package=test/{TIMESTAMP.replace(':','_')}"

logging.info(f"WRITE_BUCKET: [{WRITE_BUCKET}]")
if not WRITE_BUCKET:
    pytest.skip("no writeable bucket available", allow_module_level=True)


@pytest.fixture
def pkg():
    return QuiltPackage.FromURI(WRITE_URL)


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_push_calluri():
    uri = WRITE_URL + "_call"
    methods = QuiltPackage.METHOD_NAMES
    rmethods = list(reversed(methods))
    for method in rmethods:
        msg = f"{method}: test_push_calluri {TIMESTAMP}"
        logging.debug(msg)
        await QuiltPackage.CallURI(uri, method, msg)
    assert True


async def test_push(pkg: QuiltPackage):
    logging.debug(WRITE_URL)
    assert pkg is not None

    # Create new Package
    README = f"# Hello World!\n{TIMESTAMP}"
    logging.debug(README)
    pkg.write_text(README, "README.md")
    qpkg = await pkg.post("README")
    assert qpkg is not None

    # Read that Package
    files = await pkg.list()
    assert "README.md" in files

    # Add a file
    pkg.write_text(f"# Goodbye Cruel World!\n{TIMESTAMP}", "WRITEME.md")

    # Verify diff
    diffs = await pkg.diff()
    logging.debug(diffs)
    assert "WRITEME.md" in diffs["added"]
    logging.debug(pkg.local_files())

    # Update Whole Package
    qpkg2 = await pkg.put("WRITEME")
    assert qpkg2 is not None

    # Verify Result using legacy quilt3 APIs
    q3 = Package.browse(pkg.name, pkg.registry)
    files3 = list(q3.keys())
    assert "README.md" in files3
    assert "WRITEME.md" in files3
