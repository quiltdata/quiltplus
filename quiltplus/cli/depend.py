import asyncclick as click
import yaml
from quiltplus.package import QuiltPackage


@click.command()
@click.pass_context
@click.option(
    "-a",
    "--add-package",
    type=click.Path(),
    multiple=True,
    help="Add dependency on the URI of a package",
)
@click.option(
    "-r",
    "--remove-package",
    type=click.Path(),
    multiple=True,
    help="Remove dependency on the URI of a package",
)
@click.option(
    "-g",
    "--get-package",
    is_flag=True,
    help="Also get (install) added packages",
)
async def depend(ctx, add_package, remove_package, get_package):
    """Manage dependence on related packages"""
    cfg = ctx.obj.get("CONFIG")
    [cfg.depend(uri) for uri in add_package]
    [cfg.depend(uri, False) for uri in remove_package]
    if get_package:
        [await QuiltPackage.FromURI(uri).get() for uri in add_package]

    status = cfg.get_depend()
    click.echo(yaml.safe_dump(status))
