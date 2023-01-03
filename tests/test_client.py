from tempfile import TemporaryDirectory

from quilt3 import list_packages

from .conftest import *


@fixture
def qc():
    with TemporaryDirectory() as tmpdirname:
        qc = QuiltClient(Path(tmpdirname))
        yield qc


def setup_package(qc):
    qid = QuiltID(TEST_URL)
    pkg = qc.get(qid, K_PKG)
    pkg.get()
    return pkg


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
    with TemporaryDirectory() as tmpdirname:
        p = Path(tmpdirname)
        qc = QuiltClient(p)
        assert len(qc.recents) == 0

        for url in TEST_URLS:
            qc.get(QuiltID(url), K_PKG)
        assert len(qc.recents) == 2

        qc2 = QuiltClient(p)
        assert len(qc2.recents) == 2


def test_qc_list(qc):
    setup_package(qc)
    for p in list_packages():
        print(p)
    l = qc.list()
    assert l
    assert len(l) > 0
    assert TEST_PKG in l


def test_qc_local(qc):
    setup_package(qc)
    qid = QuiltID.Local(TEST_PKG)
    pkg = qc.get(qid, K_PKG)
    assert pkg