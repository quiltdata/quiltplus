#!/usr/bin/env python3
import anyio
import asyncclick as click


@click.group()
@click.pass_context
@click.option("--uri", help="The Quilt+ URI to operate on.")
@click.option(
    "--uri_file",
    type=click.Path(),
    default=".quilt/QUILTPLUS.shortcut",
    help="The file to read the Quilt+ URI from.",
)
async def cli(ctx, uri, uri_file):
    ctx.ensure_object(dict)
    ctx.obj["URI"] = uri
    ctx.obj["URI_FILE"] = uri_file

    pass


@cli.command()
@click.pass_context
async def echo(ctx):
    """Simple program dump out whatever is inside the context."""
    click.echo(f"ctx.obj[{ctx.obj}]")


if __name__ == "__main__":
    cli(_anyio_backend="trio")  # or asyncio
