import asyncclick as click

from .conftest import *


async def test_hello():
    await exec_hello(1, "Ernie")
    assert True
