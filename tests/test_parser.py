import pytest

from quiltplus.parser import QuiltParser

TEST_URL = "quilt+s3://quilt-example#package=examples/wellplates@fb5f3dc1b814246548dfe1492c8d00309a36e00c65b4774cbae97c5addb6359c&path=README.md"


@pytest.fixture
def qp():
    return QuiltParser()


def test_parser_init(qp):
    assert qp
    assert qp.schemas
    assert len(qp.schemas) > 2


def test_parse_uri(qp):
    uri = qp.parse_uri(TEST_URL)
    assert uri
    assert uri.registry == "s3://quilt-example"
    assert uri.package == "examples/wellplates"
    assert (
        uri.top_hash
        == "fb5f3dc1b814246548dfe1492c8d00309a36e00c65b4774cbae97c5addb6359c"
    )
    assert uri.path == "README.md"


def test_parse_package(qp):
    pkg = qp.parse_package(TEST_URL)
    assert pkg
