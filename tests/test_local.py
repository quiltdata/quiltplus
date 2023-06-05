from pathlib import Path

from pytest import raises
from quiltplus import QuiltLocal, QuiltResourceURI

from .conftest import pytestmark  # NOQA F401
from .conftest import TEST_PKG, TEST_URI, pytest


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

    opts = {QuiltLocal.K_PTH: Path(".")}
    p5 = loc.check_path(opts)
    assert p5 == p3

    p6 = loc.check_path({})
    assert p6 == p5


async def test_local_diff_get():
    qpkg = QuiltResourceURI(TEST_URI)
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

def test_local_diff_new():
    PKG=TEST_PKG+"-new"
    loc = QuiltLocal({"package": PKG})
    assert loc.local_registry
    assert PKG in str(loc.local_cache())
    diff = loc._diff()
    assert diff == {}
    assert len(diff) == 0
