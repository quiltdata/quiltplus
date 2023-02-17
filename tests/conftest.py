import logging

logging.basicConfig(level=logging.DEBUG)
from pytest import fixture, mark

from quiltplus import *

CATALOG_URL = "https://open.quiltdata.com/b/quilt-example/packages/examples/wellplates"
TEST_REG = "quilt-example"
TEST_PKG = "examples/wellplates"
TEST_URL = f"quilt+s3://{TEST_REG}#package={TEST_PKG}@fb5f3dc1b814246548dfe1492c8d00309a36e00c65b4774cbae97c5addb6359c&path=README.md&catalog=open.quiltdata.com"
REG_URL = f"quilt+s3://{TEST_REG}"
PKG_URL = f"quilt+s3://{TEST_REG}#package={TEST_PKG}"
PKG2_URL = f"quilt+s3://{TEST_REG}#package=examples/echarts"

TEST_URLS = [TEST_URL, REG_URL, PKG_URL, PKG2_URL]
