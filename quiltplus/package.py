# Resource-oriented version of a Quilt Package
# (must already exist, at least for now)

import logging
import os
import platform
import subprocess

from quilt3 import Package

from .id import *


class QuiltPackage:
    def __init__(self, id, root=Path("/tmp")):
        assert id.has_package
        cache = id.local_path()
        self.id = id
        self.root = root
        self._local_path = cache if cache else root / id.sub_path()
        self.name = id.get(K_PKG)
        self.registry = id.registry()

        self.q3pkg = (
            Package.browse(self.name)
            if (self.registry.startswith(QuiltID.LOCAL_SCHEME))
            else Package.browse(self.name, self.registry)
        )

    def __repr__(self):
        return f"QuiltPackage({self.id}, {self.root})"

    def __str__(self):
        return f"QuiltPackage[{self.name}]@{self.local_path()})"

    def local_path(self):
        return self._local_path

    def dest(self):
        return str(self._local_path)

    async def get(self, key=None):
        dest = self.dest()
        if key:
            self.q3pkg.fetch(key, dest=dest)
        else:
            self.q3pkg.fetch(dest=dest)
        return dest

    async def list(self):
        keys = self.q3pkg.keys()
        return list(keys)

    def open(self):
        dest = self.dest()
        if platform.system() == "Windows":
            os.startfile(dest)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-R", dest])
        else:
            subprocess.Popen(["xdg-open", dest])
