from asyncclick.testing import CliRunner

from ..conftest import *


async def cli_run(args, rc=0):
    runner = CliRunner()
    result = await runner.invoke(cli, args)
    logging.debug(f"run[{args}]={result}")
    assert result.exit_code == rc
    return result


async def test_cli_empty():
    result = await cli_run([])
    assert "--help" in result.output


async def test_cli_help():
    runner = CliRunner()
    result = await cli_run(["---help"], 2)
    assert "--help" in result.output


async def test_cli_no_command():
    result = await cli_run(["--uri", TEST_URL], 2)
    assert "Error: Missing command" in result.output


async def test_cli_context():
    result = await cli_run(["--uri", TEST_URL, "context"])
    assert TEST_URL in result.output


async def test_cli_pkg():
    result = await cli_run(["--uri", TEST_URL, "pkg", "-x", "list"])
    assert "README.md" in result.output
