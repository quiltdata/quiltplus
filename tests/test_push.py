from pathlib import Path
from tempfile import TemporaryDirectory

from quilt3 import Package

from .conftest import pytestmark  # NOQA F401
from .conftest import (
    SKIP_LONG_TESTS,
    TEST_URI,
    QuiltConfig,
    QuiltPackage,
    logging,
    os,
    pytest,
)

TIMESTAMP = QuiltConfig.Now()
WRITE_URI = None
WRITE_BUCKET = os.environ.get("WRITE_BUCKET")

logging.info(f"WRITE_BUCKET: [{WRITE_BUCKET}]")
if not WRITE_BUCKET:
    pytest.skip("no writeable bucket available", allow_module_level=True)


def get_pkg(prefix: str):
    WRITE_URI = (
        f"quilt+s3://{WRITE_BUCKET}#package=test/{prefix}_{TIMESTAMP.replace(':','_')}"
    )
    return QuiltPackage.FromURI(WRITE_URI)


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_push_call():
    pkg = get_pkg("test_push_call")
    methods = QuiltPackage.METHOD_NAMES
    rmethods = list(reversed(methods))
    for method in rmethods:
        msg = f"{method}: test_push_calluri {TIMESTAMP}"
        logging.debug(msg)
        await pkg.call(method, msg)
    assert True


# @pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_push_patch():
    pkg = get_pkg("test_push_patch")
    cfg = pkg.config
    with TemporaryDirectory() as tmpdirname:
        os.chdir(tmpdirname)
        key = "test.txt"
        p = Path(key)
        p.write_text(TEST_URI)
        filename = str(p)

        assert len(cfg.get_stage()) == 0
        cfg.stage(filename, True)
        assert len(cfg.get_stage()) == 1
        msg = f"test_push_patch {TIMESTAMP}"
        await pkg.post(msg)
        await pkg.patch(msg)
        assert len(cfg.get_stage()) == 0


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_push():
    pkg = get_pkg("test_push")
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
