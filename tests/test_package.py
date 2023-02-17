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
    assert len(q.keys()) == 0

    await pkg.get()
    q = await pkg.local()
    assert len(q.keys()) > 0


async def test_pkg_diff(pkg):
    diffs = await pkg.diff()
    logging.debug(f"diffs {diffs}")
    assert diffs == {"added": [], "modified": [], "deleted": []}

    await pkg.get()
    diff2 = await pkg.diff()
    logging.debug(f"diff2 {diff2}")
    assert diff2 == {"added": [], "modified": [], "deleted": []}

    pkg.save_config()
    diff3 = await pkg.diff()
    logging.debug(f"diff3 {diff3}")
    assert diff3 == {"added": [], "modified": [], "deleted": []}


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
