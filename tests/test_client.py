from tempfile import TemporaryDirectory

from .conftest import *

# get() returns recent QuiltID by numerical index
# delete(index) removes QuiltID with that index from recents
# get(index) returns Package with that index
# put(index) updates Package with that index
# post() create Package (add to recents)


@fixture
def qc():
    with TemporaryDirectory() as tmpdirname:
        qc = QuiltClient(Path(tmpdirname))
        yield qc


async def setup_package(qc):
    qid = QuiltID(TEST_URL)
    pkg = await qc.get(qid, K_PKG)
    return pkg


def test_qc(qc):
    assert qc
    assert qc.size() == 0


async def test_qc_recents(qc):
    with TemporaryDirectory() as tmpdirname:
        p = Path(tmpdirname)
        qc = QuiltClient(p)
        assert qc.size() == 0

        orig = QuiltID(TEST_URL)
        qid = await qc.post(orig.attrs)
        assert qc.size() == 1

        qlist = await qc.get()
        assert len(qlist) == 1
        assert qlist[0] == qid

        qc2 = QuiltClient(p)
        assert qc2.size() == 1


async def test_qc_id_cache(qc):
    orig = QuiltID(TEST_URL)
    assert orig.cache() == None
    qid = await qc.post(orig.attrs)
    cache = qid.cache()
    assert cache
    assert str(qc.root) in cache
    assert qid.id() in cache


async def test_qc_post(qc):
    orig = QuiltID(TEST_URL)
    attrs = orig.attrs

    qid = await qc.post(attrs)
    assert qc.size() == 1
    assert qid.id() == orig.id()

    qlist = await qc.get()
    assert len(qlist) == qc.size()
    assert qlist[0] == qid

    qget = await qc.get(qid.index)
    assert qget == qid
    assert qc.size() == 1

    qdel = await qc.delete(qid.index)
    assert qdel == qid
    assert qc.size() == 0


async def test_qc_put(qc):
    orig = QuiltID(TEST_URL)
    attrs = orig.attrs

    qid = await qc.post(attrs)
    assert qc.size() == 1
    assert qid.id() == orig.id()

    attrs["package"] = "test/client"
    del attrs["top_hash"]
    qput = await qc.put(attrs, qid.index)
    assert qc.size() == 1
    assert qput != qid
    assert qput.index == qid.index
    assert qput.id() != qid.id()

    qdel = await qc.delete(qid.index)
    assert qdel == qput
    assert qc.size() == 0


async def untest_qc_local(qc):
    await setup_package(qc)
    qid = QuiltID.Local(TEST_PKG)
    pkg = await qc.get(qid, K_PKG)
    assert pkg
