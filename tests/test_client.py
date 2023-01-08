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


async def test_qc_post(qc):
    BASE = qc.size()
    orig = QuiltID(TEST_URL)
    attrs = orig.attrs

    qid = await qc.post(attrs)
    assert qc.size() == BASE + 1
    assert qid.id() == orig.id()

    qlist = await qc.get()
    assert len(qlist) == qc.size()
    assert qlist[0] == qid

    qget = await qc.get(qid.index)
    assert qget == qid
    assert qc.size() == BASE + 1

    qdel = await qc.delete(qid.index)
    assert qdel == qid
    assert qc.size() == BASE


async def test_qc_put(qc):
    BASE = qc.size()
    orig = QuiltID(TEST_URL)
    attrs = orig.attrs

    qid = await qc.post(attrs)
    assert qc.size() == BASE + 1
    assert qid.id() == orig.id()

    attrs["package"] = "test/client"
    del attrs["top_hash"]
    qput = await qc.put(attrs, qid.index)
    assert qc.size() == BASE + 1
    assert qput != qid
    assert qput.index == qid.index
    assert qput.id() != qid.id()

    qdel = await qc.delete(qid.index)
    assert qdel == qput
    assert qc.size() == BASE


async def untest_qc_local(qc):
    await setup_package(qc)
    qid = QuiltID.Local(TEST_PKG)
    pkg = await qc.get(qid, K_PKG)
    assert pkg
