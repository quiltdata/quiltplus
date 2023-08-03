from pathlib import Path

from pytest import raises
from quiltplus import QuiltLocal, QuiltResourceURI

from .conftest import pytestmark  # NOQA F401
from .conftest import PKG_URI


def test_local_tmp():
    loc = QuiltLocal({"package": "test"})
    tmp = loc.temp_dir
    assert tmp
    p = loc.last_path
    assert p.exists()
    assert p.is_dir()


def test_local_path():
    loc = QuiltLocal({"package": "test"})
    assert loc
    p = loc.local_path()
    assert p

    p2 = loc.check_dir()
    assert p2 == p

    p3 = loc.check_dir(Path("."))
    assert p3 != p
    assert str(p3) == str(Path(".").resolve())

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
