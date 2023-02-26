import asyncclick as click


@click.command()
@click.pass_context
async def echo(ctx):
    """Simple program to dump out whatever is inside the context."""
    click.echo(f"echo ctx.obj[{ctx.obj}]")
