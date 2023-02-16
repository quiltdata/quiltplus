# Resource-oriented version of a Quilt Package
# (must already exist, at least for now)

import logging
import os
import platform
import subprocess

from quilt3 import Package

from .id import *


class QuiltPackage:
    CONFIG_FOLDER = ".quilt"
    REVISEME_FILE = "REVISEME.webloc"
    CATALOG_FILE = "CATALOG.webloc"

    @staticmethod
    def OpenLocally(dest):
        if platform.system() == "Windows":
            os.startfile(dest)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-R", dest])
        else:
            subprocess.Popen(["xdg-open", dest])
        return dest

    def __init__(self, id, root=None):
        assert id.has_package
        self.id = id
        self.name = id.get(K_PKG)
        self.registry = id.registry()

        self._local_path = root / id.sub_path() if root else id.local_path()
        # self._local_path.touch()
        self._q3pkg = None

    def __repr__(self):
        return f"QuiltPackage({self.id}, {self.root})"

    def __str__(self):
        return f"QuiltPackage[{self.name}]@{self.local_path()})"

    def local_path(self):
        p = self._local_path
        p.mkdir(parents=True, exist_ok=True)
        return p

    def local_config(self):
        p = self._local_path / QuiltPackage.CONFIG_FOLDER
        p.mkdir(parents=True, exist_ok=True)
        return p

    def dest(self):
        return str(self._local_path)

    def webloc(self, suffix=""):
        return f'{{ URL = "{self.id.catalog_uri()}{suffix}"; }}'

    def save_webloc(self, path, suffix=""):
        p = self.local_config() / path
        p.write_text(self.webloc(suffix))
        return p

    def save_config(self):
        self.save_webloc(QuiltPackage.CATALOG_FILE)
        self.save_webloc(QuiltPackage.REVISEME_FILE, "?action=revisePackage")

    def open(self):
        return QuiltPackage.OpenLocally(self.dest())

    async def browse(self):
        return (
            Package.browse(self.name)
            if (self.registry.startswith(QuiltID.LOCAL_SCHEME))
            else Package.browse(self.name, self.registry)
        )

    async def quilt(self):
        if not self._q3pkg:
            self._q3pkg = await self.browse()
        return self._q3pkg

    async def list(self):
        q = await self.quilt()
        return list(q.keys())

    async def get(self, key=None):
        dest = self.dest()
        q = await self.quilt()
        if key:
            q.fetch(key, dest=dest)
        else:
            q.fetch(dest=dest)
        return dest

    async def getAll(self):
        await self.get()
        self.save_config()
        return self.open()
