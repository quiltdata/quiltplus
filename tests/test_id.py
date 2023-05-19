from pathlib import Path

from .conftest import (
    CATALOG_URL,
    K_BKT,
    K_HSH,
    K_PKG,
    K_PRP,
    K_PTH,
    K_STR,
    K_VER,
    PKG2_URI,
    PKG_URI,
    PRP_URI,
    PTH_URI,
    REG_URI,
    TEST_BKT,
    TEST_PKG,
    TEST_URI,
    VER_URI,
    QuiltID,
    pytest,
)


@pytest.fixture
def qid():
    return QuiltID(TEST_URI)


def test_id_exists(qid: QuiltID):
    assert qid


def test_id_str(qid: QuiltID):
    u = qid.quilt_uri()
    assert u == TEST_URI
    s = str(qid)
    assert TEST_URI in s


def test_id_get(qid: QuiltID):
    assert qid.registry() == f"s3://{TEST_BKT}"
    assert qid.get(K_PKG) == TEST_PKG
    assert (
        qid.get(K_HSH)
        == "e1f83ce3dc7b9487e5732d58effabad64065d2e7401996fa5afccd0ceb92645c"
    )
    assert qid.get(K_PTH) == "README.md"


def test_id_sub_path(qid: QuiltID):
    path = Path("s3") / TEST_BKT / TEST_PKG
    assert qid.sub_path() == path
    assert qid.source_uri() == TEST_URI


def test_id_path(qid: QuiltID):
    newpath = "WRITEME.md"
    assert f"path={newpath}" in qid.path_uri(newpath)


def test_id_index(qid: QuiltID):
    n = QuiltID.INDEX
    assert n + 1 == QuiltID(TEST_URI).index
    assert n + 2 == QuiltID(REG_URI).index


def test_id_type(qid: QuiltID):
    assert QuiltID(TEST_URI).type() == K_PTH
    assert QuiltID(REG_URI).type() == K_BKT
    assert QuiltID(PKG_URI).type() == K_PKG
    assert QuiltID(PKG2_URI).type() == K_PKG
    assert QuiltID(PTH_URI).type() == K_PTH
    assert QuiltID(PRP_URI).type() == K_PRP
    assert QuiltID(VER_URI).type() == K_VER


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


def test_id_catalog(qid: QuiltID):
    print("catalog_uri", qid.catalog_uri())
    assert qid.catalog_uri() == CATALOG_URL
