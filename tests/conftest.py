import logging
import os

import pytest
from quiltplus import QuiltType

logging.basicConfig(level=logging.DEBUG)
pytestmark = pytest.mark.anyio


TEST_BKT = "quilt-example"
TEST_PKG = "examples/wellplates"

CATALOG_URL = f"https://open.quiltdata.com/b/{TEST_BKT}/packages/{TEST_PKG}"
TEST_URI = (
    f"quilt+s3://{TEST_BKT}#package={TEST_PKG}"
    + "@e1f83ce3dc7b9487e5732d58effabad64065d2e7401996fa5afccd0ceb92645c"
    + "&path=README.md&catalog=open.quiltdata.com"
)
BKT_URI = f"quilt+s3://{TEST_BKT}"
PKG_URI = f"quilt+s3://{TEST_BKT}#{QuiltType.K_PKG}={TEST_PKG}@e1f83ce3dc7b"
PKG2_URI = f"quilt+s3://{TEST_BKT}#{QuiltType.K_PKG}=examples/echarts:latest"
PTH_URI = f"quilt+s3://{TEST_BKT}#{QuiltType.K_PKG}={TEST_PKG}&{QuiltType.K_PTH}=README.md"
PRP_URI = f"quilt+s3://{TEST_BKT}#{QuiltType.K_PKG}={TEST_PKG}&{QuiltType.K_PTH}=README.md&{QuiltType.K_PRP}=*"
VER_URI = f"quilt+s3://{TEST_BKT}#{QuiltType.K_PKG}={TEST_PKG}"

TEST_URIS = [TEST_URI, BKT_URI, PKG_URI, PKG2_URI, PTH_URI, PRP_URI, VER_URI]

SKIP_LONG_TESTS = os.environ.get("SKIP_LONG_TESTS")
print("SKIP_LONG_TESTS {SKIP_LONG_TESTS}")
