from .conftest import *


@fixture
def pkg():
    qid = QuiltID(TEST_URL)
    pkg = QuiltPackage(qid)
    return pkg


def test_pkg_fixture(pkg):
    assert pkg


async def test_pkg_list(pkg):
    files = await pkg.list()
    assert files
    assert len(files) > 3
    assert "README.md" in files


async def test_pkg_local(pkg):
    q = await pkg.local()
    assert q is not None
    qkeys = q.keys()
    assert qkeys is not None
    qlist = list(qkeys)
    assert len(qlist) == 0
    

@mark.skip(reason="unready")
async def test_pkg_diff(pkg):
    diffs = await pkg.diff()
    assert diffs
    # assert len(files) > 3
    # assert "README.md" in files


async def test_pkg_get(pkg):
    rc = await pkg.get()
    assert rc


async def test_pkg_open(pkg):
    rc = await pkg.get()
    assert rc
    pkg.save_config()
    pkg.open()


async def test_pkg_getAll(pkg):
    rc = await pkg.getAll()
    assert rc
