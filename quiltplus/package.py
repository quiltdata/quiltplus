from pathlib import Path

from quilt3 import Package

ROOT = Path.home() / "Documents" / "QuiltData"


class QuiltPackage:
    def __init__(self, uri, root=ROOT):
        self.uri = uri
        self.root = root / uri.package
        self.pkg = Package.browse(self.uri.package, self.uri.registry)

    def get(self):
        self.pkg.fetch(dest=self.root)
        return self.root

    def list(self):
        keys = self.pkg.keys()
        return list(keys)
