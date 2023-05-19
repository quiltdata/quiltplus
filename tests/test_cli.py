from asyncclick.testing import CliRunner

from .conftest import TEST_URI, cli, logging, pytestmark  # NOQA F401


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
    result = await cli_run(["---help"], 2)
    assert "--help" in result.output


async def test_cli_no_command():
    result = await cli_run(["--uri", TEST_URI], 2)
    assert "Error: Missing command" in result.output


async def test_cli_catalog():
    result = await cli_run(["-U", TEST_URI, "catalog"])
    assert "http" in result.output


async def test_cli_context():
    result = await cli_run(["--uri", TEST_URI, "context"])
    assert TEST_URI in result.output


async def test_cli_depend():
    result = await cli_run(["--uri", TEST_URI, "depend"])
    assert result


async def test_cli_pkg():
    result = await cli_run(["--uri", TEST_URI, "pkg", "-x", "list"])
    assert "README.md" in result.output


async def test_cli_stage():
    result = await cli_run(["--uri", TEST_URI, "stage"])
    assert "stage" in result.output
