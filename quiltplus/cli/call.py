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
    uri = ctx.obj.get("URI")
    if not uri:
        click.echo(f"ERROR: NO_URI_FOUND\n{ctx.obj}")
    logging.debug(f"call[{message}] {method} {uri}")
    result = await QuiltPackage.CallURI(uri, method, message)
    click.echo(result)
