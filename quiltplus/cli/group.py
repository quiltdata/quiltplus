#!/usr/bin/env python3

import logging

import anyio
import asyncclick as click

from quiltplus.config import QuiltConfig

from .call import call
from .echo import echo


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


cli.add_command(echo)
cli.add_command(call)
