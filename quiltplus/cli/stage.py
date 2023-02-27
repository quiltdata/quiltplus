import logging

import asyncclick as click
import yaml


@click.command()
@click.pass_context
@click.option(
    "-a",
    "--add-file",
    type=click.Path(),
    multiple=True,
    help="Stage adding/updating file to package",
)
@click.option(
    "-r",
    "--remove-file",
    type=click.Path(),
    multiple=True,
    help="Stage removing file from package",
)
async def stage(ctx, add_file, remove_file):
    """Stage file"""
    cfg = ctx.obj.get("CONFIG")
    [cfg.stage(file) for file in add_file]
    [cfg.stage(file, False) for file in remove_file]

    status = cfg.get_stage()
    click.echo(yaml.safe_dump(status))
