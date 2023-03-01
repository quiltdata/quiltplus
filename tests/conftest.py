import logging

logging.basicConfig(level=logging.DEBUG)

import os

import pytest

from quiltplus import (K_BKT, K_HSH, K_PKG, K_PTH, K_STR, GitIgnore,
                       QuiltConfig, QuiltID, QuiltIdCache, QuiltPackage, cli)

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "trio"


CATALOG_URL = "https://open.quiltdata.com/b/quilt-example/packages/examples/wellplates"
TEST_BKT = "quilt-example"
TEST_PKG = "examples/wellplates"
TEST_URL = f"quilt+s3://{TEST_BKT}#package={TEST_PKG}@fb5f3dc1b814246548dfe1492c8d00309a36e00c65b4774cbae97c5addb6359c&path=README.md&catalog=open.quiltdata.com"
REG_URL = f"quilt+s3://{TEST_BKT}"
PKG_URL = f"quilt+s3://{TEST_BKT}#package={TEST_PKG}"
PKG2_URL = f"quilt+s3://{TEST_BKT}#package=examples/echarts"

TEST_URLS = [TEST_URL, REG_URL, PKG_URL, PKG2_URL]

SKIP_LONG_TESTS = os.environ.get("SKIP_LONG_TESTS")
