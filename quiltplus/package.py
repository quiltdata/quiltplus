from pathlib import Path

from quilt3 import Package

ROOT = Path.home() / "Documents" / "QuiltData"


class QuiltPackage:
    def __init__(self, uri, root=ROOT):
        self.uri = uri
        self.root = root / uri.package
        self.pkg = Package()

    def install(self):
        self.pkg.install(self.uri.package, self.uri.registry, dest=self.root)
        return True
