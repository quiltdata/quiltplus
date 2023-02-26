#!/usr/bin/env python3
import logging

import anyio
import asyncclick as click

from quiltplus.config import QuiltConfig
from quiltplus.package import QuiltPackage


@click.group()
@click.pass_context
@click.option("-u", "--uri", help="The Quilt+ URI to operate on.")
@click.option(
    "-f",
    "--config-file",
    type=click.Path(),
    default=QuiltConfig.CONFIG_FOLDER,
    show_default=True,
    help="The file to read the Quilt+ URI from.",
)
async def cli(ctx, uri, config_file):
    ctx.ensure_object(dict)
    ctx.obj["URI"] = uri if uri else cli_uri(config_file)
    return ctx.obj


def cli_uri(config_file):
    cfg = QuiltConfig(config_file)
    logging.debug(f"cli_uri.cfg: {cfg}")
    return cfg.get_uri()


@cli.command()
@click.pass_context
@click.option(
    "-x",
    "--method",
    default="get",
    show_default=True,
    type=click.Choice(QuiltPackage.METHOD_NAMES, case_sensitive=False),
)
@click.option("-m", "--message", help="commit message")
async def call(ctx, method, message):
    """Call async methods on package object."""
    uri = ctx.obj.get("URI")
    if not uri:
        click.echo(f"ERROR: NO_URI_FOUND\n{ctx.obj}")
    logging.debug(f"call[{message}] {method} {uri}")
    result = await QuiltPackage.CallURI(uri, method, message)
    click.echo(result)


@cli.command()
@click.pass_context
async def echo(ctx):
    """Simple program to dump out whatever is inside the context."""
    click.echo(f"echo ctx.obj[{ctx.obj}]")


if __name__ == "__main__":
    cli(_anyio_backend="trio")  # or asyncio
