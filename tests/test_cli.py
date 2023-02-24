from asyncclick.testing import CliRunner

from .conftest import *


async def test_hello():
    await exec_hello(1, "Ernie")
    assert True


async def test_hello_runner():
    runner = CliRunner()
    result = await runner.invoke(hello, ["--name", "Peter"])
    assert result.exit_code == 0
    assert result.output == "Hello, Peter!\n"
