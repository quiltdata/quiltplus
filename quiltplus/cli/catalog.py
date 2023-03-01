import webbrowser

import asyncclick as click
from quiltplus.config import QuiltConfig


@click.command()
@click.pass_context
@click.option(
    "-r",
    "--revise-package",
    is_flag=True,
    help="Revise package in catalog (instead of just viewing it)",
)
async def catalog(ctx, revise_package):
    """Open package in a Quilt catalog."""
    cfg = ctx.obj.get("CONFIG")
    key = QuiltConfig.K_REV if revise_package else QuiltConfig.K_CAT
    url = cfg.get_uri(key)
    if not url:
        click.echo(f"ERROR: CATALOG_URL_NOT_FOUND\n{ctx.obj}")
        return
    click.echo(url)
    webbrowser.open(url)
