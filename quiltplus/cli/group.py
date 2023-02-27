#!/usr/bin/env python3

import logging

import anyio
import asyncclick as click

from quiltplus.config import QuiltConfig
from quiltplus.package import QuiltPackage

from .call import call
from .echo import echo
from .stage import stage


@click.group()
@click.pass_context
@click.option("-u", "--uri", help="Use this Quilt+ URI.")
@click.option("-U", "--update-uri", help="Update config and use this Quilt+ URI.")
@click.option(
    "-f",
    "--config-file",
    type=click.Path(),
    default=QuiltConfig.CONFIG_FOLDER,
    show_default=True,
    help="The file to read the Quilt+ URI from.",
)
async def cli(ctx, uri, update_uri, config_file):
    ctx.ensure_object(dict)
    cfg = QuiltConfig(config_file)

    if update_uri:
        cfg.update_config(uri=update_uri)
    actual_uri = uri or cfg.get_uri()

    if actual_uri:
        pkg = QuiltPackage.FromURI(actual_uri)
        pkg.config = cfg
        ctx.obj["URI"] = actual_uri
        ctx.obj["PKG"] = pkg
    ctx.obj["CONFIG"] = cfg

    return ctx.obj


cli.add_command(echo)
cli.add_command(call)
cli.add_command(stage)
