from quiltplus import (
    QuiltPackage,
    QuiltPath,
    QuiltProperty,
    QuiltRegistry,
    QuiltResourceURI,
    QuiltVersions,
)

from .conftest import pytestmark  # NOQA F401
from .conftest import (
    BKT_URI,
    PKG_URI,
    PRP_URI,
    PTH_URI,
    SKIP_LONG_TESTS,
    VER_URI,
    pytest,
)


async def test_res_pkg():
    qpkg = QuiltResourceURI(PKG_URI)
    assert isinstance(qpkg, QuiltPackage)


async def test_res_reg():
    qreg = QuiltResourceURI(BKT_URI)
    assert isinstance(qreg, QuiltRegistry)


async def test_res_path():
    qr = QuiltResourceURI(PTH_URI)
    assert isinstance(qr, QuiltPath)


async def test_res_prop():
    qr = QuiltResourceURI(PRP_URI)
    assert isinstance(qr, QuiltProperty)


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_res_reg_list():
    qreg = QuiltResourceURI(BKT_URI)
    result = await qreg.list()
    assert len(result) > 0
    first = result[0]
    assert ":latest" in first
    assert "package=" in first


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_res_ver_list():
    qr = QuiltResourceURI(VER_URI)
    assert isinstance(qr, QuiltVersions)
    result = await qr.list()
    assert len(result) > 0
    assert "@" in result[0]


async def test_res_path_get():
    qr = QuiltResourceURI(PTH_URI)
    assert isinstance(qr, QuiltPath)
    results = await qr.get()
    assert len(results) > 0

