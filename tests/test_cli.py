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
    result = await runner.invoke(cli, ["--name", "Peter"])
    print(result)
    assert "Error: Missing command" in result.output
    assert result.exit_code == 2


async def test_cli_greet():
    runner = CliRunner()
    result = await runner.invoke(cli, ["--name", "Peter", "greet"])
    print(result)
    assert "Hello, Peter!" in result.output
    assert result.exit_code == 0
