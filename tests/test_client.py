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
    uri = qid.raw
    assert qc.recents[uri]
