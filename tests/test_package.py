import pytest

from quiltplus.parser import QuiltParser

TEST_URL = "quilt+s3://quilt-example#package=examples/wellplates@fb5f3dc1b814246548dfe1492c8d00309a36e00c65b4774cbae97c5addb6359c&path=README.md"


@pytest.fixture
def pkg():
    qp = QuiltParser()
    pkg = qp.parse_package(TEST_URL)
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
