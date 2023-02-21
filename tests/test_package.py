from .conftest import *

RM_LOCAL = os.path.join(QuiltPackage.CONFIG_FOLDER, QuiltPackage.REVISEME_FILE)


@pytest.fixture
def pkg():
    return QuiltPackage.FromURI(TEST_URL)


def test_pkg_fixture(pkg: QuiltPackage):
    assert pkg

def test_pkg_str(pkg: QuiltPackage):
    s = str(pkg)
    assert pkg.name in s
    logging.debug(pkg)


async def test_pkg_empty(pkg: QuiltPackage):
    assert pkg is not None
    l = await pkg.local()
    assert l is not None
    q = await pkg.quilt()
    assert q is not None


async def test_pkg_write(pkg: QuiltPackage):
    p = pkg.write_text("abc", "test.txt")
    assert "test.txt" in str(p)
    assert "abc" == p.read_text()

    p2 = pkg.write_text("abc", "test.txt", "parent")
    path = os.path.join("parent", "test.txt")
    assert path in str(p2)


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_pkg_local(pkg: QuiltPackage):
    q = await pkg.local()
    assert len(q.keys()) == 0

    await pkg.get()
    q = await pkg.local()
    assert len(q.keys()) > 0


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_pkg_local_files(pkg: QuiltPackage):
    assert pkg.local_files() == []
    await pkg.get()
    assert pkg.local_files() != []
    assert "README.md" in pkg.local_files()
    pkg.save_config()
    assert RM_LOCAL in pkg.local_files()


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_pkg_diff(pkg: QuiltPackage):
    diffs = await pkg.diff()
    assert diffs == {"added": [], "modified": [], "deleted": []}

    await pkg.get()
    diff2 = await pkg.diff()
    assert diff2 == {"added": [], "modified": [], "deleted": []}

    pkg.save_config()
    diff3 = await pkg.diff()
    assert diff3 != {"added": [], "modified": [], "deleted": []}
    adds = diff3["added"]
    assert adds != []
    assert RM_LOCAL in adds


async def test_pkg_list(pkg: QuiltPackage):
    files = await pkg.list()
    assert files
    assert len(files) > 3
    assert "README.md" in files


async def test_pkg_changed(pkg: QuiltPackage):
    dfiles = await pkg.list(True)
    print(dfiles)
    assert len(dfiles) == 0

    pkg.save_config()
    print(dfiles)
    dfiles = await pkg.list(True)
    assert RM_LOCAL in dfiles


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_pkg_get(pkg: QuiltPackage):
    rc = await pkg.get()
    assert rc


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_pkg_open(pkg: QuiltPackage):
    rc = await pkg.get()
    assert rc
    pkg.save_config()
    pkg.open()


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_pkg_getAll(pkg: QuiltPackage):
    rc = await pkg.getAll()
    assert rc
