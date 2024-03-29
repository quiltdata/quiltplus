from quiltplus import QuiltUri

from .conftest import (
    BKT_URI,
    PKG_URI,
    PRP_URI,
    PTH_URI,
    TEST_BKT,
    TEST_PKG,
    TEST_URI,
    VER_URI,
    pytest,
)


@pytest.fixture
def uri():
    return QuiltUri.FromUri(TEST_URI)


def test_uri(uri: QuiltUri):
    assert uri.uri == TEST_URI
    assert uri.registry == f"s3://{TEST_BKT}"
    assert uri.package == TEST_PKG


def test_uri_repr(uri: QuiltUri):
    assert TEST_URI in repr(uri)
    assert uri == uri


def test_uri_eq(uri: QuiltUri):
    assert uri == uri
    uri_pth = QuiltUri.FromUri(PTH_URI)
    assert uri_pth == uri
    uri_bkt = QuiltUri.FromUri(BKT_URI)
    assert uri_bkt != uri


TYPE_URIS = {
    QuiltUri.K_PKG: PKG_URI,
    QuiltUri.K_PRP: PRP_URI,
    QuiltUri.K_PTH: PTH_URI,
    QuiltUri.K_BKT: BKT_URI,
    QuiltUri.K_VER: VER_URI,
}


def test_uri_types():
    for key, uri in TYPE_URIS.items():
        attrs = QuiltUri.AttrsFromUri(uri)
        assert QuiltUri.Type(attrs) == key


def test_uri_null():
    un = QuiltUri({})
    assert un
    assert un.uri is None
