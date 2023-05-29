from quiltplus import QuiltPackage, QuiltRegistry, QuiltResourceURI, QuiltVersions

from .conftest import pytestmark  # NOQA F401
from .conftest import BKT_URI, PKG_URI, SKIP_LONG_TESTS, VER_URI, pytest


async def test_res_pkg():
    qpkg = QuiltResourceURI(PKG_URI)
    assert isinstance(qpkg, QuiltPackage)


async def test_res_reg():
    qreg = QuiltResourceURI(BKT_URI)
    assert isinstance(qreg, QuiltRegistry)


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_res_reg_list():
    qreg = QuiltResourceURI(BKT_URI)
    assert isinstance(qreg, QuiltRegistry)
    result = await qreg.list()
    assert len(result) > 0
    first = result[0]
    assert ":latest" in first
    assert "package=" in first


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_res_ver_list():
    qreg = QuiltResourceURI(VER_URI)
    assert isinstance(qreg, QuiltVersions)
    result = await qreg.list()
    assert len(result) > 0
    assert "@" in result[0]
