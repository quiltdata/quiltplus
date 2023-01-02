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


def test_id_type(qid):
    assert qid.type() == K_PTH


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
