from .conftest import *


@fixture
def pkg():
    qid = QuiltID(TEST_URL)
    pkg = QuiltPackage(qid)
    return pkg


def test_pkg_fixture(pkg):
    assert pkg


def test_pkg_get(pkg):
    rc = pkg.get()
    assert rc


def test_pkg_list(pkg):
    files = pkg.list()
    assert files
    assert len(files) > 3
    assert "README.md" in files
