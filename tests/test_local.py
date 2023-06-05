from pathlib import Path
from pytest import raises
from quiltplus import QuiltLocal

from .conftest import TEST_PKG, pytest


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

@pytest.mark.skip(reason="Must first download a package to diff")    
def test_local_diff():
    loc = QuiltLocal({"package":TEST_PKG})
    assert loc.local_registry
    assert TEST_PKG in str(loc.local_cache())
    diff = loc._diff()
    assert diff
    assert isinstance(diff, dict)
    for uri, stage in diff.items():
        assert stage in ("add", "rm", "touch")
        assert stage == "rm"
