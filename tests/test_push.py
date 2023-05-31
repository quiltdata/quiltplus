import logging
import os
from pathlib import Path

from quilt3 import Package
from quiltplus import QuiltLocal, QuiltPackage

from .conftest import pytestmark  # NOQA F401
from .conftest import SKIP_LONG_TESTS, TEST_URI, pytest

TIMESTAMP = QuiltPackage.Now()
WRITE_URI = None
WRITE_BUCKET = os.environ.get("WRITE_BUCKET")

logging.info(f"WRITE_BUCKET: [{WRITE_BUCKET}]")
if not WRITE_BUCKET:
    pytest.skip("no writeable bucket available", allow_module_level=True)


def get_unique_pkg(prefix: str):
    WRITE_URI = (
        f"quilt+s3://{WRITE_BUCKET}#package=test/{prefix}_{TIMESTAMP.replace(':','_')}"
    )
    return QuiltPackage.FromURI(WRITE_URI)


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_push_patch():
    pkg = get_unique_pkg("test_push_patch")
    for tmpdirname in QuiltLocal.TempDir():
        os.chdir(tmpdirname)
        key = "test.txt"
        p = Path(key)
        p.write_text(TEST_URI)
        str(p)
        opts = {"message": f"{__name__} {TIMESTAMP}"}
        result = await pkg.patch(opts)
        assert result is not None


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_push_put():
    pkg = get_unique_pkg("test_push")
    assert pkg is not None

    # Create new Package
    README = f"# Hello World!\n{TIMESTAMP}"
    logging.debug(README)
    pkg.write_text(README, "README.md")
    opts = {"message": f"{__name__} {README}"}
    qpkg = await pkg.put(opts)
    assert qpkg is not None

    # Read that Package
    files = await pkg.list()
    assert "README.md" in files

    # Add a file
    WRITEME = f"# Goodbye Cruel World!\n{TIMESTAMP}"
    pkg.write_text(WRITEME, "WRITEME.md")

    # Verify diff
    diffs = await pkg.diff()
    logging.debug(diffs)
    assert "WRITEME.md" in diffs["added"]
    logging.debug(pkg.local_files())

    # Update Whole Package
    opts2 = {"message": f"{__name__} {WRITEME}"}
    qpkg2 = await pkg.put(opts2)
    assert qpkg2 is not None

    # Verify Result using legacy quilt3 APIs
    q3 = Package.browse(pkg.package, pkg.registry)
    files3 = list(q3.keys())
    assert "README.md" in files3
    assert "WRITEME.md" in files3


@pytest.mark.skip(reason="Not implemented")
async def test_push_call():
    pkg = get_unique_pkg("test_push_call")
    methods = QuiltPackage.METHOD_NAMES
    rmethods = list(reversed(methods))
    for method in rmethods:
        msg = f"{method}: test_push_calluri {TIMESTAMP}"
        logging.debug(msg)
        await pkg.call(method, msg)
    assert True
