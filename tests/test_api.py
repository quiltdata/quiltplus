from quiltplus import get_package, get_registry, list_package, list_registry  # NOQA F401

from .conftest import TEST_BKT, TEST_PKG


def test_api_get_registry():
    assert get_registry(TEST_BKT) is not None


def test_api_list_registry():
    assert list_registry(TEST_BKT) is not None


def test_api_get_package():
    assert get_package(TEST_BKT, TEST_PKG) is not None


def test_api_list_package():
    assert list_package(TEST_BKT, TEST_PKG) is not None
