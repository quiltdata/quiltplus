import asyncclick as click
import yaml


@click.command()
@click.pass_context
async def context(ctx):
    """Simple program to dump out whatever is inside the context."""
    click.echo("context")
    click.echo(yaml.safe_dump(ctx.obj))
