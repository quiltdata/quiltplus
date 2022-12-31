from quilt3 import Package

from .id import *


class QuiltPackage:
    def __init__(self, id, root=Path("/tmp")):
        self.id = id
        self.dest = root / id.get(K_ID)
        self.name = id.get(K_PKG)
        self.pkg = Package.browse(self.name, id.get(K_REG))

    def get(self):
        self.pkg.fetch(dest=self.dest)
        return self.dest

    def list(self):
        keys = self.pkg.keys()
        return list(keys)
