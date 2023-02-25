from asyncclick.testing import CliRunner

from .conftest import *


async def test_cli_empty():
    runner = CliRunner()
    result = await runner.invoke(cli, [])
    print(result)
    assert "--help" in result.output
    assert result.exit_code == 0


async def test_cli_help():
    runner = CliRunner()
    result = await runner.invoke(cli, ["---help"])
    print(result)
    assert "--help" in result.output
    assert result.exit_code == 2


async def test_cli_no_command():
    runner = CliRunner()
    result = await runner.invoke(cli, ["--uri", TEST_URL])
    print(result)
    assert "Error: Missing command" in result.output
    assert result.exit_code == 2


async def test_cli_echo():
    runner = CliRunner()
    result = await runner.invoke(cli, ["--uri", TEST_URL, "echo"])
    print(result)
    assert TEST_URL in result.output
    assert result.exit_code == 0
