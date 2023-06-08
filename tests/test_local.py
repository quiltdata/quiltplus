import os
import sys
from pathlib import Path

from pytest import raises
from quiltplus import QuiltLocal, QuiltResourceURI

from .conftest import pytestmark  # NOQA F401
from .conftest import PKG_URI, TEST_PKG, pytest


def test_local_tmp():
    for tmp in QuiltLocal.TempDir():
        assert tmp
        assert isinstance(tmp, Path)
        assert tmp.exists()


def test_local_path():
    loc = QuiltLocal({"package": "test"})
    assert loc
    p = loc.local_path()
    assert p

    p2 = loc.check_dir()
    assert p2 == p

    p3 = loc.check_dir(Path("."))
    assert p3 != p
    assert str(p3) == "."

    p4 = loc.check_dir(Path("test_nonexistent/"))
    assert p4

    with raises(ValueError):
        loc.check_dir(Path("README.md"))

    opts = {QuiltLocal.K_DIR: Path(".")}
    p5 = loc.check_dir_arg(opts)
    assert p5 == p3

    p6 = loc.check_dir_arg({})
    assert p6 == p5


def test_local_files():
    NEW_FILE = "test.txt"
    loc = QuiltResourceURI(PKG_URI)
    assert loc
    files = loc.local_files()
    assert len(files) == 0

    loc.write_text("abc", NEW_FILE)
    files = loc.local_files()
    assert len(files) == 1
    file0 = files[0]
    assert file0 == loc.local_path() / NEW_FILE


@pytest.mark.skipif(os.getenv("GITHUB_ACTIONS") == "true", reason="does not work in CI")
async def test_local_diff_get():
    qpkg = QuiltResourceURI(PKG_URI)
    await qpkg.get()
    loc = QuiltLocal({"package": TEST_PKG})
    assert loc.local_registry
    assert TEST_PKG in str(loc.local_cache())
    diff = loc._diff()
    assert diff
    assert isinstance(diff, dict)
    assert len(diff) > 0
    for uri, stage in diff.items():
        assert stage in ("add", "rm", "touch")
        assert stage == "rm"


@pytest.mark.skipif(sys.platform.startswith("win"), reason="tmp folder name issue")
def test_local_diff_new():
    PKG = TEST_PKG + "-new"
    loc = QuiltLocal({"package": PKG})
    assert loc.local_registry
    assert PKG in str(loc.local_cache())
    diff = loc._diff()
    assert diff == {}
    assert len(diff) == 0
