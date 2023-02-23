from urllib.parse import urlencode, urlunparse

from .conftest import *


@pytest.fixture
def qid():
    return QuiltID(TEST_URL)


def test_id_exists(qid: QuiltID):
    assert qid


def test_id_str(qid: QuiltID):
    u = qid.quilt_uri()
    assert u == TEST_URL
    s = str(qid)
    assert TEST_URL in s


def test_id_get(qid: QuiltID):
    assert qid.registry() == f"s3://{TEST_BKT}"
    assert qid.get(K_PKG) == TEST_PKG
    assert (
        qid.get(K_HSH)
        == "fb5f3dc1b814246548dfe1492c8d00309a36e00c65b4774cbae97c5addb6359c"
    )
    assert qid.get(K_PTH) == "README.md"


def test_id_sub_path(qid: QuiltID):
    path = Path("s3") / TEST_BKT / TEST_PKG
    assert qid.sub_path() == path
    assert qid.source_uri() == TEST_URL


def test_id_index(qid: QuiltID):
    n = QuiltID.INDEX
    assert n + 1 == QuiltID(TEST_URL).index
    assert n + 2 == QuiltID(REG_URL).index


def test_id_type(qid: QuiltID):
    assert qid.type() == K_PTH


def test_id_from_attrs(qid: QuiltID):
    assert qid.attrs
    url2 = QuiltID.FromAttrs(qid.attrs).source_uri()
    assert qid.source_uri() == url2


def test_id_with_keys(qid: QuiltID):
    result = qid.with_keys("id", "a", "b")
    assert result
    assert isinstance(result, dict)
    assert result["id"] == qid.index
    assert result["a"] == qid.get(K_PKG)
    assert result["b"] == qid.source_uri()


def test_id_local():
    qid = QuiltID.Local(TEST_PKG)
    check = {
        K_STR: QuiltID.LOCAL_SCHEME,
        K_BKT: QuiltID.LOCAL_HOST,
        K_PKG: TEST_PKG,
    }
    assert qid

    for key in check.keys():
        assert qid.get(key) == check[key]


async def test_id_catalog(qid: QuiltID):
    url = qid.catalog_uri()
    assert url
    assert url == CATALOG_URL
