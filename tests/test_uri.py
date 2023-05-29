from pathlib import Path
from udc import UnUri

from .conftest import pytestmark  # NOQA F401
from .conftest import (
    TEST_BKT,
    TEST_PKG,
    PKG_URI,
    PRP_URI,
    PTH_URI,
    BKT_URI,
    TEST_URI,
    VER_URI,
    QuiltUri,
    pytest,
)

@pytest.fixture
def uri():
    un = UnUri(TEST_URI)
    return QuiltUri(un.attrs)

def test_uri(uri: QuiltUri):
    assert uri.uri == TEST_URI
    assert uri.registry == f"s3://{TEST_BKT}"
    assert uri.pkg == TEST_PKG

TYPE_URIS = {
    QuiltUri.K_PKG: PKG_URI,
    QuiltUri.K_PRP: PRP_URI,
    QuiltUri.K_PTH: PTH_URI,
    QuiltUri.K_BKT: BKT_URI,
    QuiltUri.K_VER: VER_URI,
}
