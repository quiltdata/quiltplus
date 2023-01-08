from urllib.parse import urlencode, urlunparse

from .conftest import *


@fixture
def qid():
    return QuiltID(TEST_URL)


def test_id_exists(qid):
    assert qid
    assert K_REG


def test_id_get(qid):
    assert qid.get(K_REG) == f"s3://{TEST_REG}"
    assert qid.get(K_PKG) == TEST_PKG
    assert (
        qid.get(K_HSH)
        == "fb5f3dc1b814246548dfe1492c8d00309a36e00c65b4774cbae97c5addb6359c"
    )
    assert qid.get(K_PTH) == "README.md"


def test_id_id(qid):
    path = Path("s3") / TEST_REG / TEST_PKG
    assert qid.get(K_ID) == str(path)
    assert qid.get(K_PID) == path
    assert qid.get(K_RAW) == TEST_URL


def test_id_index(qid):
    n = QuiltID.INDEX
    assert n + 1 == QuiltID(TEST_URL).index
    assert n + 2 == QuiltID(REG_URL).index


def test_id_type(qid):
    assert qid.type() == K_PTH


def test_id_from_attrs(qid):
    assert qid.attrs
    url2 = QuiltID.FromAttrs(qid.attrs).source()
    print(url2)
    assert qid.source() == QuiltID.Decode(url2)


def test_id_with_keys(qid):
    result = qid.with_keys("id", "a", "b")
    assert result
    assert isinstance(result, dict)
    assert result["id"] == qid.index
    assert result["a"] == qid.get(K_PKG)
    assert result["b"] == qid.source()


def test_id_local():
    qid = QuiltID.Local(TEST_PKG)
    check = {
        K_REG: f"{QuiltID.LOCAL_SCHEME}://{QuiltID.LOCAL_HOST}",
        K_STR: QuiltID.LOCAL_SCHEME,
        K_HNM: QuiltID.LOCAL_HOST,
        K_PKG: TEST_PKG,
    }
    assert qid
    for key in check.keys():
        assert qid.get(key) == check[key]
