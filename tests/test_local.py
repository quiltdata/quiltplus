from pathlib import Path

from udc import UnUri

from quiltplus import QuiltLocal


def test_local_tmp():
    for tmp in QuiltLocal.TempDir():
        print(tmp)
        print(dir(tmp))
        assert tmp
        assert isinstance(tmp, Path)
        assert tmp.exists()

def test_local_path():
    loc = QuiltLocal({"package": "test"})
    assert loc

