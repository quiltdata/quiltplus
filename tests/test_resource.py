from .conftest import pytestmark  # NOQA F401
from .conftest import (
    PKG_URI,
    REG_URI,
    SKIP_LONG_TESTS,
    VER_URI,
    QuiltPackage,
    QuiltRegistry,
    QuiltResource,
    pytest,
)


async def test_res_types():
    pkg: QuiltPackage = QuiltPackage.FromURI(PKG_URI)
    assert isinstance(pkg, QuiltPackage)


async def test_res_pkg():
    qpkg = QuiltResource(PKG_URI)
    assert isinstance(qpkg, QuiltPackage)


async def test_res_reg():
    qreg = QuiltResource(REG_URI)
    assert isinstance(qreg, QuiltRegistry)


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_res_reg_list():
    qreg = QuiltResource(REG_URI)
    assert isinstance(qreg, QuiltRegistry)
    result = await qreg.list()
    assert len(result) > 0
    first = result[0]
    assert ":latest" in first
    assert "package=" in first


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_res_ver_list():
    qreg = QuiltResource(VER_URI)
    result = await qreg.list()
    assert len(result) > 0
    assert "@" in result[0]
