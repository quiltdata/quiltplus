#!/usr/bin/env python3
import anyio
import asyncclick as click

from .config import QuiltConfig


@click.group()
@click.pass_context
@click.option("--uri", help="The Quilt+ URI to operate on.")
@click.option(
    "--config_file",
    type=click.Path(),
    default=".quilt/config.yaml",
    help="The file to read the Quilt+ URI from.",
)
@click.option(
    "--config_folder",
    type=click.Path(),
    default=".quilt",
    help="The folder containing the configurational YAML.",
)
async def cli(ctx, uri, config_file, config_folder):
    ctx.ensure_object(dict)
    ctx.obj["URI"] = uri
    ctx.obj["CONFIG_FILE"] = config_file
    ctx.obj["CONFIG_FOLDER"] = config_folder
    ctx.obj["URIS"] = cli_uris(ctx.obj)


def cli_uris(obj):
    if "URI" in obj:
        return [obj["URI"]]
    return []


@cli.command()
@click.pass_context
async def echo(ctx):
    """Simple program to dump out whatever is inside the context."""
    click.echo(f"echo ctx.obj[{ctx.obj}]")


if __name__ == "__main__":
    cli(_anyio_backend="trio")  # or asyncio
