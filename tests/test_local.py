from pathlib import Path
from pytest import raises

from quiltplus import QuiltLocal


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

    p4 = loc.check_dir(Path("test_nonexistent"))
    assert p4

    with raises(ValueError):
        loc.check_dir(Path("README.md"))

