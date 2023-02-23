# Resource-oriented version of a Quilt Package
# (must already exist, at least for now)

import logging
import os
import platform
import shutil
import subprocess

from quilt3 import Package

from .id import *


class QuiltPackage:
    CONFIG_FOLDER = ".quilt"
    REVISEME_FILE = "REVISEME.webloc"
    CATALOG_FILE = "CATALOG.webloc"

    @staticmethod
    def FromURI(url_string: str):
        qid = QuiltID(url_string)
        pkg = QuiltPackage(qid)
        return pkg

    @staticmethod
    def OpenLocally(dest: str):
        if platform.system() == "Windows":
            os.startfile(dest)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-R", dest])
        else:
            subprocess.Popen(["xdg-open", dest])
        return dest

    def __init__(self, id: QuiltID, root=None):
        assert id.has_package
        self.id = id
        self.name = id.get(K_PKG)
        self.registry = id.registry()

        self._local_path = root / id.sub_path() if root else id.local_path()
        self._q3pkg = None
        self._q3local = None

    def __repr__(self):
        return f"QuiltPackage[{self.id}]@{self.local_path()})"

    def __str__(self):
        return self.__repr__()

    def local_path(self, *paths: str):
        p = self._local_path
        for path in paths:
            p = p / path

        p.mkdir(parents=True, exist_ok=True)
        return p

    def local_files(self):
        root = self.local_path()
        return [
            os.path.relpath(os.path.join(dir, file), root)
            for (dir, dirs, files) in os.walk(root)
            for file in files
        ]

    def dest(self):
        return str(self.local_path())  # + "/"

    def webloc(self, suffix=""):
        return f'{{ URL = "{self.id.catalog_uri()}{suffix}"; }}'

    def shortcut(self, suffix=""):
        return f"[InternetShortcut]\nURL={self.id.catalog_uri()}{suffix}"

    def write_text(self, text: str, file: str, *paths: str):
        dir = self.local_path(*paths)
        p = dir / file
        p.write_text(text)
        return p

    def save_webloc(self, file: str, suffix=""):
        url_file = file.replace("webloc", ".URL")
        path = self.write_text(
            self.shortcut(suffix), url_file, QuiltPackage.CONFIG_FOLDER
        )
        path = self.write_text(self.webloc(suffix), file, QuiltPackage.CONFIG_FOLDER)
        return path

    def save_config(self):
        self.save_webloc(QuiltPackage.CATALOG_FILE)
        self.save_webloc(QuiltPackage.REVISEME_FILE, "?action=revisePackage")

    def open(self):
        return QuiltPackage.OpenLocally(self.dest())

    async def browse(self):
        q = (
            Package.browse(self.name)
            if (self.registry.startswith(QuiltID.LOCAL_SCHEME))
            else Package.browse(self.name, self.registry)
        )
        q.set_dir(".", path=self.dest())
        return q

    async def local(self):
        q = Package().set_dir(".", path=self.dest())
        return q

    async def quilt(self):
        try:
            if not self._q3pkg:
                self._q3pkg = await self.browse()
            else:
                self._q3pkg.browse(self.name)
            return self._q3pkg
        except Exception as err:
            logging.error(err)
        return await self.local()

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
        print(f"diff: {diffs}")
        return {"added": diffs[0], "modified": diffs[1], "deleted": diffs[2]}

    async def get(self, key=None):
        dest = self.dest()
        q = await self.quilt()
        if key:
            q.fetch(key, dest=dest)
        else:
            q.fetch(dest=dest)
        return dest

    async def put(self, msg=None):  # create new package from scratch
        q = await self.local()
        q.set_dir(".", path=self.dest())
        q.build(self.name)
        result = q.push(self.name, registry=self.registry, message=msg)
        return result

    async def post(self, msg=None):  # update existing package
        q = await self.quilt()
        q.set_dir(".", path=self.dest())
        q.build(self.name)
        result = q.push(self.name, registry=self.registry, message=msg)
        return result

    def delete(self):  # remove local cache
        shutil.rmtree(self._local_path)
        return result

    async def getAll(self):
        await self.get()
        self.save_config()
        return self.open()
