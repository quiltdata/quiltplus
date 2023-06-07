import logging

from .package import QuiltPackage


class QuiltPath(QuiltPackage):
    def __init__(self, attrs: dict):
        super().__init__(attrs)
        self.path = attrs[QuiltPath.K_PTH]
        logging.debug(f"QuiltPath {self.path} @ {self.uri}")

    async def get(self, opts: dict = {}):
        dir_dest = self.check_path(opts)
        dest = dir_dest / self.path
        q = await self.remote_pkg()
        qp = q[self.path]
        qp.fetch(dest=dest)
        return [self.uri]
