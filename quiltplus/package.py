# Resource-oriented version of a Quilt Package
# (must already exist, at least for now)

import logging
import os
import platform
import shutil
import subprocess

from quilt3 import Package

from .config import QuiltConfig
from .id import K_PKG, QuiltID


class QuiltPackage:
    METHOD_NAMES = "get list diff patch put post".split(" ")

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
        self.name = id.pkg()
        self.registry = id.registry()
        self._local_path = root / id.sub_path() if root else id.local_path()
        self.config = QuiltConfig.ForRoot(self._local_path)

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

    def write_text(self, text: str, file: str, *paths: str):
        dir = self.local_path(*paths)
        p = dir / file
        p.write_text(text)
        return p

    def save_uri(self):
        self.config.save_uri(self.id)

    def open(self):
        return QuiltPackage.OpenLocally(self.dest())

    async def browse(self):
        try:
            q = (
                Package.browse(self.name, top_hash=self.id.hash())
                if (self.registry.startswith(QuiltID.LOCAL_SCHEME))
                else Package.browse(self.name, self.registry, top_hash=self.id.hash())
            )
            return q
        except Exception as err:
            logging.error(err)
        return None

    async def local(self):
        q = Package().set_dir(".", path=self.dest())
        return q

    async def remote(self):
        return await self.browse()

    async def list(self, changed_only=False):
        if changed_only:
            diffs = await self.diff()
            return [x for sub in diffs.values() for x in sub]
        q = await self.remote()
        return list(q.keys())

    async def diff(self):
        logging.debug(f"\ndiff.local_files\n{self.local_files()}")
        q_remote = await self.remote()
        logging.debug(f"diff.remote_keys {q_remote.keys()}")
        q_local = await self.local()
        logging.debug(f"diff.local_keys {q_local.keys()}")
        diffs = q_remote.diff(q_local)
        logging.debug(f"diff: {diffs}")
        return {"added": diffs[0], "modified": diffs[1], "deleted": diffs[2]}

    async def get(self, key=None):
        dest = self.dest()
        q = await self.remote()
        if key:
            q.fetch(key, dest=dest)
        else:
            q.fetch(dest=dest)
        return dest

    async def post(self, msg=None):  # create new empty package
        q = await self.local()
        q.build(self.name)
        result = q.push(self.name, registry=self.registry, message=msg)
        return result

    async def put(self, msg=None):  # update using all local files
        q = await self.remote()
        q.set_dir(".", path=self.dest())
        q.build(self.name)
        result = q.push(self.name, registry=self.registry, message=msg)
        return result

    async def patch(self, msg=None):  # update only staged files
        q = await self.remote()
        [q.set(f) for f in self.config.get_stage(adds=True)]
        [q.delete(f) for f in self.config.get_stage(adds=False)]
        q.build(self.name)
        print(q)
        result = q.push(self.name, registry=self.registry, message=msg)
        self.config.update_config({}, reset_stage=True)
        return result

    def delete(self):  # remove local cache
        return shutil.rmtree(self._local_path)

    async def getAll(self):
        await self.get()
        self.save_uri()
        return self.open()

    async def call(self, method: str = "get", msg: str = ""):
        if msg == "":
            msg = f"{QuiltConfig.Now()} {method} {self})"
        attr_method = getattr(self, method)
        return await attr_method(msg) if method[0] == "p" else await attr_method()
