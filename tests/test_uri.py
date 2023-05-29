from udc import UnUri

from .conftest import pytestmark  # NOQA F401
from .conftest import (BKT_URI, PKG_URI, PRP_URI, PTH_URI, TEST_BKT, TEST_PKG,
                       TEST_URI, VER_URI, QuiltUri, pytest)


@pytest.fixture
def uri():
    return QuiltUri.FromUri(TEST_URI)

def test_uri(uri: QuiltUri):
    assert uri.uri == TEST_URI
    assert uri.registry == f"s3://{TEST_BKT}"
    assert uri.package == TEST_PKG

TYPE_URIS = {
    QuiltUri.K_PKG: PKG_URI,
    QuiltUri.K_PRP: PRP_URI,
    QuiltUri.K_PTH: PTH_URI,
    QuiltUri.K_BKT: BKT_URI,
    QuiltUri.K_VER: VER_URI,
}

def test_uri_types():
    for key, uri in TYPE_URIS.items():
        un = UnUri(uri)
        assert QuiltUri.Type(un.attrs) == key