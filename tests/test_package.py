import logging
import os

from quiltplus import QuiltPackage

from .conftest import pytestmark  # NOQA F402
from .conftest import SKIP_LONG_TESTS, TEST_URI, pytest


def assert_diffs(diffs, a, m, d):
    assert len(diffs["added"]) == a
    # assert len(diffs["modified"]) == m # Ignore (environment-dependent)
    assert len(diffs["deleted"]) == d
    return diffs


@pytest.fixture
def pkg():
    return QuiltPackage.FromURI(TEST_URI)


def test_pkg_fixture(pkg: QuiltPackage):
    assert pkg


def test_pkg_str(pkg: QuiltPackage):
    s = str(pkg)
    assert pkg.package in s
    logging.debug(pkg)


async def test_pkg_empty(pkg: QuiltPackage):
    assert pkg is not None
    loc = await pkg.local_pkg()
    assert loc is not None
    loc2 = await pkg.local_pkg()
    assert loc2 is not None

    q = await pkg.remote_pkg()
    assert q is not None
    q2 = await pkg.remote_pkg()  # re-browse
    assert q2 is not None


async def test_pkg_write(pkg: QuiltPackage):
    pkg.check_dir()
    p = pkg.write_text("abc", "test.txt")
    assert "test.txt" in str(p)
    assert "abc" == p.read_text()

    p2 = pkg.write_text("abc", "test.txt", "parent")
    path = os.path.join("parent", "test.txt")
    assert path in str(p2)


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_pkg_local(pkg: QuiltPackage):
    q = await pkg.local_pkg()
    assert len(q.keys()) == 0

    await pkg.get()
    q = await pkg.local_pkg()
    assert len(q.keys()) > 0


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_pkg_local_files(pkg: QuiltPackage):
    assert pkg.local_files() == []
    await pkg.get()
    assert pkg.local_files() != []
    assert "README.md" in pkg.local_files()


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_pkg_diff(pkg: QuiltPackage):
    # new remote package
    assert_diffs(await pkg.diff(), 0, 0, 7)

    # installed package
    await pkg.get()
    assert_diffs(await pkg.diff(), 0, 0, 0)

    # added files
    TEST_FILE = "test.txt"
    pkg.write_text(TEST_FILE, TEST_FILE)
    diff3 = assert_diffs(await pkg.diff(), 1, 0, 0)
    adds = diff3["added"]
    assert TEST_FILE in adds


async def test_pkg_child(pkg: QuiltPackage):
    files = await pkg.child()
    assert files
    assert len(files) > 3
    assert "README.md" in files
    assert "render.html" not in files


async def test_pkg_list(pkg: QuiltPackage):
    files = await pkg.list()
    assert files
    assert len(files) > 3
    assert pkg.package in files[0]


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_pkg_get(pkg: QuiltPackage):
    rc = await pkg.get()
    assert rc
