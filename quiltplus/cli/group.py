#!/usr/bin/env python3

import asyncclick as click
from quiltplus.config import QuiltConfig
from quiltplus.package import QuiltPackage

from .catalog import catalog
from .context import context
from .depend import depend
from .pkg import pkg
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
    ctx.obj["CONFIG"] = cfg

    actual_uri = uri or update_uri or cfg.get_uri()
    if actual_uri:
        pkg = QuiltPackage.FromURI(actual_uri)
        pkg.config = cfg
        if update_uri:
            pkg.save_uri()
        ctx.obj["URI"] = actual_uri
        ctx.obj["PKG"] = pkg

    return ctx.obj


cli.add_command(pkg)
cli.add_command(stage)
cli.add_command(depend)
cli.add_command(catalog)
cli.add_command(context)
