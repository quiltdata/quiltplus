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
async def pkg(ctx, method, message):
    """Call async methods on package object."""
    qpkg = ctx.obj.get("PKG")
    if not qpkg:
        click.echo(f"ERROR: NO_PACKAGE_GIVEN\n{ctx.obj}")
        return
    logging.debug(f"pkg[{message}] {method} {qpkg}")
    result = await qpkg.call(method, message)
    click.echo(result)
