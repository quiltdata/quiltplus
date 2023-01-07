from .conftest import *


@fixture
def pkg():
    qid = QuiltID(TEST_URL)
    pkg = QuiltPackage(qid)
    return pkg


def test_pkg_fixture(pkg):
    assert pkg


async def test_pkg_get(pkg):
    rc = await pkg.get()
    assert rc


async def test_pkg_list(pkg):
    files = await pkg.list()
    assert files
    assert len(files) > 3
    assert "README.md" in files
