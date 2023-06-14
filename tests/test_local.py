import os
import sys
from pathlib import Path

from pytest import raises
from quiltplus import QuiltLocal, QuiltResourceURI

from .conftest import pytestmark  # NOQA F401
from .conftest import PKG_URI, TEST_PKG, pytest


def test_local_tmp():
    loc = QuiltLocal({"package": "test"})
    tmp = loc.temp_dir
    assert tmp
    p = loc.dir_path
    assert p.exists()
    assert p.is_dir()


def test_local_files():
    NEW_FILE = "test.txt"
    loc = QuiltResourceURI(PKG_URI)
    assert loc
    files = loc.local_files()
    assert len(files) == 0

    loc.write_text("abc", NEW_FILE)
    files = loc.local_files()
    assert len(files) == 1
    file0 = files[0]
    assert file0 == loc.local_path() / NEW_FILE


@pytest.mark.skipif(os.getenv("GITHUB_ACTIONS") == "true", reason="does not work in CI")
async def test_local_diff_get():
    qpkg = QuiltResourceURI(PKG_URI)
    await qpkg.get()
    loc = QuiltLocal({"package": TEST_PKG})
    assert loc.local_registry
    assert TEST_PKG in str(loc.local_cache())
    diff = loc._diff()
    assert diff
    assert isinstance(diff, dict)
    assert len(diff) > 0
    for uri, stage in diff.items():
        assert stage in ("add", "rm", "touch")
        assert stage == "rm"


@pytest.mark.skipif(sys.platform.startswith("win"), reason="tmp folder name issue")
def test_local_diff_new():
    PKG = TEST_PKG + "-new"
    loc = QuiltLocal({"package": PKG})
    assert loc.local_registry
    assert PKG in str(loc.local_cache())
    diff = loc._diff()
    assert diff == {}
    assert len(diff) == 0
