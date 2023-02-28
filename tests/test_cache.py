from tempfile import TemporaryDirectory

from .conftest import (TEST_URL, Generator, Path, QuiltID, QuiltIdCache,
                       TemporaryDirectory, pytest, pytestmark)

# get() returns recent QuiltID by numerical index
# delete(index) removes QuiltID with that index from recents
# get(index) returns Package with that index
# put(index) updates Package with that index
# post() create Package (add to recents)


@pytest.fixture
def qc():
    with TemporaryDirectory() as tmpdirname:
        qc = QuiltIdCache(Path(tmpdirname))
        yield qc
        qc.save_qids()


async def setup_package(qc):
    qid = QuiltID(TEST_URL)
    pkg = await qc.get(qid, K_PKG)
    return pkg


def test_qc(qc: Generator[QuiltIdCache, None, None]):
    assert qc
    assert qc.size() == 0


async def test_qc_str(qc: Generator[QuiltIdCache, None, None]):
    with TemporaryDirectory() as tmpdirname:
        p = Path(tmpdirname)
        qc = QuiltIdCache(p)
        assert tmpdirname in str(qc)
        qc.save_qids()


async def test_qc_saved(qc: Generator[QuiltIdCache, None, None]):
    with TemporaryDirectory() as tmpdirname:
        p = Path(tmpdirname)
        qc = QuiltIdCache(p)
        assert qc.cache_file.exists() == True
        assert not qc.dirty

        qc.save_qids()
        assert not qc.dirty


async def test_qc_reload(qc: Generator[QuiltIdCache, None, None]):
    with TemporaryDirectory() as tmpdirname:
        p = Path(tmpdirname)
        qc = QuiltIdCache(p)
        assert qc.size() == 0

        orig = QuiltID(TEST_URL)
        qid = await qc.post(orig.attrs)
        assert qc.size() == 1

        qlist = await qc.get()
        assert len(qlist) == 1
        assert qlist[0] == qid

        qc.save_qids()
        qc2 = QuiltIdCache(p)
        assert qc2.size() == 1
        qc2.save_qids()


async def test_qc_id_local_path(qc: Generator[QuiltIdCache, None, None]):
    orig = QuiltID(TEST_URL)
    qid = await qc.post(orig.attrs)
    cache = qid.local_path()
    assert cache
    assert str(qc.root) in str(cache)
    assert str(qid.sub_path()) in str(cache)


async def test_qc_post(qc: Generator[QuiltIdCache, None, None]):
    orig = QuiltID(TEST_URL)
    attrs = orig.attrs

    qid = await qc.post(attrs)
    assert qc.size() == 1

    qlist = await qc.get()
    assert len(qlist) == qc.size()
    assert qlist[0] == qid

    qget = await qc.get(qid.index)
    assert qget == qid
    assert qc.size() == 1

    qdel = await qc.delete(qid.index)
    assert qdel == qid
    assert qc.size() == 0


async def test_qc_put(qc: Generator[QuiltIdCache, None, None]):
    orig = QuiltID(TEST_URL)
    attrs = orig.attrs

    qid = await qc.post(attrs)
    assert qc.size() == 1

    attrs["package"] = "test/cache"
    del attrs["top_hash"]
    qput = await qc.put(attrs, qid.index)
    assert qc.size() == 1
    assert qput != qid
    assert qput.index == qid.index

    qdel = await qc.delete(qid.index)
    assert qdel == qput
    assert qc.size() == 0


async def untest_qc_local_path(qc):
    await setup_package(qc)
    qid = QuiltID.Local(TEST_PKG)
    pkg = await qc.get(qid, K_PKG)
    assert pkg
