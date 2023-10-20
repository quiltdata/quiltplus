import logging
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from quilt3 import Package  # type: ignore
from quiltplus import QuiltPackage, QuiltType

from .conftest import pytestmark  # NOQA F401
from .conftest import SKIP_LONG_TESTS, TEST_URI, pytest

TIMESTAMP = QuiltPackage.Now()
WRITE_URI = None
WRITE_BUCKET = os.environ.get("WRITE_BUCKET") or False

logging.info(f"WRITE_BUCKET: [{WRITE_BUCKET}]")
if not WRITE_BUCKET:
    pytest.skip("no writeable bucket available", allow_module_level=True)


def get_unique_pkg(prefix: str):
    WRITE_URI = f"quilt+s3://{WRITE_BUCKET}#package=test/{prefix}_{QuiltType.Now()}"
    return QuiltPackage.FromURI(WRITE_URI)


@pytest.fixture
def tmpdir():
    with TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_push_patch(tmpdir: Path):
    pkg = get_unique_pkg("test_push_patch")
    key = "test.txt"
    p = tmpdir / key
    p.write_text(TEST_URI)
    str(p)
    opts = {
        QuiltPackage.K_MSG: f"{__name__} {TIMESTAMP}",
        QuiltPackage.K_DIR: tmpdir,
    }
    result = await pkg.patch(opts)
    assert result is not None


@pytest.mark.skip("Not fully implemented")
def test_push_core_commit(tmpdir: Path):  # pragma: no cover
    name = "test_push_core_commit"
    pkg = get_unique_pkg(name)
    cache = tmpdir / name
    pkg.assign_dir(cache)
    man = pkg.commit()
    assert man


def check_file(file: str, uris: list[str]) -> bool:
    return sum(1 for uri in uris if file in uri) == 1


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
@pytest.mark.skip(reason="unexpected keyword argument 'workflow'")
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
    assert check_file("README.md", files)

    # Add a file
    WRITEME = f"# Goodbye Cruel World!\n{TIMESTAMP}"
    pkg.write_text(WRITEME, "WRITEME.md")

    # Verify diff
    # diffs = await pkg.diff()
    # logging.debug(diffs)
    # assert "WRITEME.md" in diffs["added"]
    # logging.debug(pkg.local_files())

    # Update Whole Package
    opts2 = {"message": f"{__name__} {WRITEME}"}
    qpkg2 = await pkg.put(opts2)
    assert qpkg2 is not None

    # Verify Result using legacy quilt3 APIs
    q3 = Package.browse(pkg.package, pkg.registry)
    files3 = list(q3.keys())
    assert check_file("README.md", files3)
    assert check_file("WRITEME.md", files3)
