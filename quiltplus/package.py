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
    def FromURI(url_string):
        qid = QuiltID(url_string)
        pkg = QuiltPackage(qid)
        return pkg

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
        self._q3pkg = None
        self._q3local = None

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

    def local_files(self, pattern="*"):
        root = self.local_path()
        return [
            os.path.relpath(os.path.join(dir, file), root)
            for (dir, dirs, files) in os.walk(root)
            for file in files
        ]

    def dest(self):
        return str(self.local_path()) + "/"

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
        p = (
            Package.browse(self.name)
            if (self.registry.startswith(QuiltID.LOCAL_SCHEME))
            else Package.browse(self.name, self.registry)
        )
        return p

    async def local(self):
        q3local = Package().set_dir(".", path=self.dest())
        q3local.build(self.name)
        return q3local

    async def quilt(self):
        if not self._q3pkg:
            self._q3pkg = await self.browse()
        else:
            self._q3pkg.browse(self.name)
        return self._q3pkg

    async def list(self, changed_only=False):
        if changed_only:
            diffs = await self.diff()
            return [x for sub in diffs.values() for x in sub]
        q = await self.quilt()
        return list(q.keys())

    async def diff(self):
        q_remote = await self.quilt()
        q_local = await self.local()
        diffs = q_remote.diff(q_local)
        return {"added": diffs[0], "modified": diffs[1], "deleted": diffs[0]}

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
