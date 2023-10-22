from quiltplus import get_package, get_registry, list_package, list_registry  # NOQA F401

from .conftest import TEST_BKT, TEST_PKG


async def test_api_get_registry():
    assert await get_registry(TEST_BKT) is not None


async def test_api_list_registry():
    assert await list_registry(TEST_BKT) is not None


async def test_api_get_package():
    assert await get_package(TEST_BKT, TEST_PKG) is not None


async def test_api_list_package():
    assert await list_package(TEST_BKT, TEST_PKG) is not None
