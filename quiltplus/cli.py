#!/usr/bin/env python3
import anyio
import asyncclick as click


@click.group()
@click.pass_context
@click.option("--name", prompt="Your name", help="The person to greet.")
async def cli(ctx, name):
    ctx.ensure_object(dict)
    ctx.obj["NAME"] = name
    click.echo(f"cli.context[{ctx}]")
    pass


@cli.command()
@click.pass_context
async def greet(ctx):
    """Simple program that greets NAME for a total of COUNT times."""
    name = ctx.obj["NAME"]
    click.echo(f"Hello, {name}!")


if __name__ == "__main__":
    cli(_anyio_backend="trio")  # or asyncio
