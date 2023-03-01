import asyncclick as click
import yaml
from quiltplus.ignore import GitIgnore


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
@click.option(
    "-i",
    "--ignore-files",
    is_flag=True,
    help="Add staged file(s) to gitignore if not present (reverse if removed)",
)
# NOTE: Should we git-ignore files by default? Then unignore them too?
async def stage(ctx, add_file, remove_file, ignore_files):
    """Stage file"""
    cfg = ctx.obj.get("CONFIG")
    [cfg.stage(file) for file in add_file]
    [cfg.stage(file, False) for file in remove_file]
    if ignore_files:
        gi = GitIgnore()
        gi.ignore(add_file)
        gi.unignore(remove_file)
        gi.save()

    status = cfg.get_stage()
    click.echo(yaml.safe_dump(status))
