#!/usr/bin/env python3

from quiltplus.cli import cli

if __name__ == "__main__":
    cli(_anyio_backend="trio")  # or asyncio
