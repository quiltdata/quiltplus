import logging
import os

from quiltplus import QuiltPackage

from .conftest import pytestmark  # NOQA F402
from .conftest import FORCE, SKIP_LONG_TESTS, PKG_URI, TEST_URI, pytest


def assert_diffs(diffs, a, m, d):
    assert len(diffs["added"]) == a
    # assert len(diffs["modified"]) == m # Ignore (environment-dependent)
    assert len(diffs["deleted"]) == d
    return diffs


@pytest.fixture
def pkg():
    return QuiltPackage.FromURI(PKG_URI)


def test_pkg_fixture(pkg: QuiltPackage):
    assert pkg


def test_pkg_str(pkg: QuiltPackage):
    s = str(pkg)
    pkg_name = pkg.package or ""
    assert pkg_name in s


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


@pytest.mark.skipif(os.getenv("GITHUB_ACTIONS") == "true", reason="does not work in CI")
async def test_pkg_diff(pkg: QuiltPackage):
    staged = pkg.stage_uri("diff", "README.md")
    assert staged.startswith("quilt+stage+diff")
    assert staged.endswith("README.md")

    await pkg.get()
    diffs = await pkg.diff({})
    assert diffs
    assert len(diffs) > 0
    d0 = diffs[0]
    assert isinstance(d0, str)
    assert d0.startswith("quilt+stage+rm")


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
    pkg_name = pkg.package or ""
    assert pkg_name in files[0]


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_pkg_get(pkg: QuiltPackage):
    rc = await pkg.get()
    assert rc
