import os
import platform
import subprocess

from quilt3 import Package

from .id import *


class QuiltPackage:
    def __init__(self, id, root=Path("/tmp")):
        cache = id.cache()
        self.id = id
        self.dest = cache if cache else root / id.get(K_ID)
        self.name = id.get(K_PKG)
        self.registry = id.get(K_REG)

        self.pkg = (
            Package.browse(self.name)
            if (self.registry.startswith(QuiltID.LOCAL_SCHEME))
            else Package.browse(self.name, self.registry)
        )

    async def get(self):
        self.pkg.fetch(dest=self.dest)
        return self.dest

    async def list(self):
        keys = self.pkg.keys()
        return list(keys)

    async def open(self):
        if platform.system() == "Windows":
            os.startfile(self.dest)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-R", self.dest])
        else:
            subprocess.Popen(["xdg-open", self.dest])
