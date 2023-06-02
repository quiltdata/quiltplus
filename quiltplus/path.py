import logging
from pathlib import Path

from .package import QuiltPackage


class QuiltPath(QuiltPackage):
    def __init__(self, attrs: dict):
        super().__init__(attrs)
        self.path = attrs[QuiltPath.K_PTH]
        logging.debug(f"QuiltPath {self.path} @ {self.uri}")

    async def get(self, opts: dict = {}):
        dest = self.dest()
        q = await self.remote_pkg()
        q.fetch(self.path, dest=dest)
        return dest
