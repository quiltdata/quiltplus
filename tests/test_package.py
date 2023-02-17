from .conftest import *

RM_LOCAL = os.path.join(QuiltPackage.CONFIG_FOLDER, QuiltPackage.REVISEME_FILE)

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


async def test_pkg_changed(pkg):
    dfiles = await pkg.list(True)
    print(dfiles)
    assert len(dfiles) == 0

    pkg.save_config()
    print(dfiles)
    dfiles = await pkg.list(True)
    assert RM_LOCAL in dfiles


async def test_pkg_local(pkg):
    q = await pkg.local()
    assert len(q.keys()) == 0

    await pkg.get()
    q = await pkg.local()
    assert len(q.keys()) > 0


async def test_pkg_local_files(pkg):
    assert pkg.local_files() == []
    await pkg.get()
    assert pkg.local_files() != []
    assert 'README.md' in pkg.local_files()
    pkg.save_config()
    assert RM_LOCAL in pkg.local_files()


async def test_pkg_diff(pkg):
    diffs = await pkg.diff()
    assert diffs == {"added": [], "modified": [], "deleted": []}

    await pkg.get()
    diff2 = await pkg.diff()
    assert diff2 == {"added": [], "modified": [], "deleted": []}

    pkg.save_config()
    diff3 = await pkg.diff()
    assert diff3 != {"added": [], "modified": [], "deleted": []}
    adds = diff3['added']
    assert adds != []
    assert RM_LOCAL in adds


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
