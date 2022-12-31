from tempfile import TemporaryDirectory

from .conftest import *


@fixture
def qc():
    with TemporaryDirectory() as tmpdirname:
        qc = QuiltClient(Path(tmpdirname))
        yield qc


def test_qc(qc):
    assert qc
    assert qc.recents == {}


def test_qc_get(qc):
    qid = QuiltID(TEST_URL)
    pkg = qc.get(qid, K_PKG)
    assert isinstance(pkg, QuiltPackage)
    key = qid.id()
    assert qc.recents[key]


def test_qc_recents(qc):
    REG_URL = "quilt+s3://quilt-example"
    PKG_URL = "quilt+s3://quilt-example#package=examples/wellplates"
    PKG2_URL = "quilt+s3://quilt-example#package=examples/echarts"

    assert len(qc.recents) == 0

    for url in [TEST_URL, REG_URL, PKG_URL, PKG2_URL]:
        print(url)
        qid = QuiltID(url)
        pkg = qc.get(qid, K_PKG)
        print(qc.recents.keys())

    assert len(qc.recents) == 2
