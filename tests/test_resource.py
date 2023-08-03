from quiltcore import Namespace, Registry
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
    FIRST_PKG,
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


def test_res_reg_core():
    qreg = QuiltResourceURI(BKT_URI)
    assert qreg.domain is not None
    assert isinstance(qreg.domain, Registry)
    names = qreg.domain.list()
    assert len(names) > 0
    assert names[0].name == FIRST_PKG


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_res_reg_list():
    qreg = QuiltResourceURI(BKT_URI)
    result = await qreg.list()
    assert len(result) > 0
    first = result[0]
    assert ":latest" in first
    assert f"package={FIRST_PKG}" in first


async def test_res_ver_core():
    qr = QuiltResourceURI(VER_URI)
    print(qr.domain)
    print(f"qr.package={qr.package}")
    ns = qr.domain.get(qr.package)
    assert ns is not None
    assert isinstance(ns, Namespace)
    print(f"ns={ns} -> {ns.manifests}")
    assert ns.get("latest") is not None


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_res_ver_list():
    qr = QuiltResourceURI(VER_URI)
    assert isinstance(qr, QuiltVersions)
    result = await qr.list()
    assert len(result) > 0
    assert "@" in result[0]


@pytest.mark.skipif(SKIP_LONG_TESTS, reason="Skip long tests")
async def test_res_path_get():
    qr = QuiltResourceURI(PTH_URI)
    assert isinstance(qr, QuiltPath)
    results = await qr.get()
    assert len(results) > 0
