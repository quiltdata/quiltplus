import logging

import asyncclick as click

from quiltplus.package import QuiltPackage


@click.command()
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
    pkg = ctx.obj.get("PKG")
    if not pkg:
        click.echo(f"ERROR: NO_PACKAGE_FOUND\n{ctx.obj}")
    logging.debug(f"call[{message}] {method} {pkg}")
    result = await pkg.call(method, message)
    click.echo(result)
