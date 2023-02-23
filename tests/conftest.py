import os

CI_ENVIRONMENT = os.environ.get("GITHUB_WORKSPACE")
if CI_ENVIRONMENT:
    os.environ["XDG_CACHE_HOME"] = CI_ENVIRONMENT
    import quilt3

import logging
import time
from typing import Generator

import pytest

from quiltplus import *

logging.basicConfig(level=logging.DEBUG)

CATALOG_URL = "https://open.quiltdata.com/b/quilt-example/packages/examples/wellplates"
TEST_BKT = "quilt-example"
TEST_PKG = "examples/wellplates"
TEST_URL = f"quilt+s3://{TEST_BKT}#package={TEST_PKG}@fb5f3dc1b814246548dfe1492c8d00309a36e00c65b4774cbae97c5addb6359c&path=README.md&catalog=open.quiltdata.com"
REG_URL = f"quilt+s3://{TEST_BKT}"
PKG_URL = f"quilt+s3://{TEST_BKT}#package={TEST_PKG}"
PKG2_URL = f"quilt+s3://{TEST_BKT}#package=examples/echarts"

TEST_URLS = [TEST_URL, REG_URL, PKG_URL, PKG2_URL]

SKIP_LONG_TESTS = os.environ.get("SKIP_LONG_TESTS")
