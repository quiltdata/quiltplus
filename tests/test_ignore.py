from .conftest import GitIgnore, pytest

TEST_FILE = "foobar.$$$"


@pytest.fixture
def gi():
    return GitIgnore()


def test_gi_lines(gi):
    assert gi
    assert gi.lines()
    assert len(gi.lines()) > 0


def test_gi_add_rm(gi):
    n = gi.size()
    assert TEST_FILE not in gi.lines()

    gi.ignore([TEST_FILE])
    assert gi.size() == n + 1
    assert TEST_FILE in gi.lines()
    assert TEST_FILE in gi.text()

    gi.unignore([TEST_FILE])
    assert gi.size() == n
    assert TEST_FILE not in gi.lines()
    assert TEST_FILE not in gi.text()
