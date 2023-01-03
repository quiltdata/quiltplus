import os
import pathlib
import shutil
import sys
import tempfile
from functools import partial
from unittest import mock

import pytest


# Module Vars / Constants
class Vars:
    tmpdir_factory = None
    tmpdir_home = None
    tmpdir_data = None
    extrasession_mockers = []


def pytest_sessionstart(session):
    """pytest_sessionstart hook

    This runs *before* import and collection of tests.

    This is *THE* place to do mocking of things that are global,
    such as `platformdirs`.

    Do teardown in `pytest_sessionfinish()`
    """
    print("Pre-Session Setup..")
    # Looks like there's no public API to get the resolved value of pytest base temp dir
    # (https://docs.pytest.org/en/6.2.x/tmpdir.html#the-default-base-temporary-directory).
    Vars.tmpdir_home = pathlib.Path(tempfile.mkdtemp(prefix="pytest-fake_home"))
    Vars.tmpdir_data = Vars.tmpdir_home / "platformdirs_datadir"
    Vars.tmpdir_data.mkdir()
    Vars.tmpdir_cache = Vars.tmpdir_home / "platformdirs_cachedir"
    Vars.tmpdir_cache.mkdir()

    def get_dir(*args, d):
        return str(d / args[0] if args else d)

    # Mockers that need to be loaded before any of our code
    Vars.extrasession_mockers.extend(
        [
            mock.patch(
                "platformdirs.user_data_dir", partial(get_dir, d=Vars.tmpdir_data)
            ),
            mock.patch(
                "platformdirs.user_cache_dir", partial(get_dir, d=Vars.tmpdir_cache)
            ),
        ]
    )

    for mocker in Vars.extrasession_mockers:
        mocker.start()


def pytest_sessionfinish(session, exitstatus):
    """pytest_sessionfinish hook

    This runs *after* any finalizers or other session activities.

    Performs teardown for `pytest_sessionstart()`
    """
    print("\nPost-session Teardown..")

    shutil.rmtree(Vars.tmpdir_home)
    for mocker in Vars.extrasession_mockers:
        mocker.stop()


# scope: function, class, module, or session
# autouse: boolean.  Apply to all instances of the given scope.
@pytest.fixture(scope="session", autouse=True)
def each_session(request):
    print("\nSetup session..")

    def teardown():  # can be named whatever
        print("\nTeardown session..")

    request.addfinalizer(teardown)


@pytest.fixture(scope="function", autouse=True)
def set_temporary_working_dir(request, tmpdir):
    print("Setting tempdir to {}".format(tmpdir))
    orig_dir = os.getcwd()
    os.chdir(tmpdir)

    def teardown():  # can be named whatever
        print("Unsetting tempdir..")
        os.chdir(orig_dir)

    request.addfinalizer(teardown)


@pytest.fixture
def isolate_packages_cache(tmp_path):
    with mock.patch("quilt3.packages.CACHE_PATH", tmp_path):
        yield


@pytest.fixture
def clear_data_modules_cache():
    to_remove = [
        name for name in sys.modules if name.split(".")[:2] == ["quilt3", "data"]
    ]
    for name in to_remove:
        del sys.modules[name]


from pytest import fixture

from quiltplus.client import *
from quiltplus.id import *
from quiltplus.package import *

TEST_REG = "quilt-example"
TEST_PKG = "examples/wellplates"
TEST_URL = f"quilt+s3://{TEST_REG}#package={TEST_PKG}@fb5f3dc1b814246548dfe1492c8d00309a36e00c65b4774cbae97c5addb6359c&path=README.md"
REG_URL = f"quilt+s3://{TEST_REG}"
PKG_URL = f"quilt+s3://{TEST_REG}#package={TEST_PKG}"
PKG2_URL = f"quilt+s3://{TEST_REG}#package=examples/echarts"

TEST_URLS = [TEST_URL, REG_URL, PKG_URL, PKG2_URL]

# https://github.com/quiltdata/quilt/blob/master/api/python/tests/conftest.py#L33-L37
