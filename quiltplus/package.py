# Resource-oriented version of a Quilt Package

import logging
import os
import platform
import shutil
import subprocess

from quilt3 import Package

from .config import QuiltConfig
from .id import QuiltID
from .parse import K_HSH
from .root import QuiltRoot


class QuiltPackage(QuiltRoot):
    METHOD_NAMES = "get list diff patch put".split(" ")

    @staticmethod
    def FromURI(url_string: str):
        qid = QuiltID(url_string)
        pkg = QuiltPackage(qid.attrs)
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

    def __init__(self, attrs: dict, root=None):
        super().__init__(attrs)
        self._local_path = root / attrs["sub_path"] if root else attrs["local_path"]
        self.config = QuiltConfig.ForRoot(self._local_path)
        self.hash = self.attrs.get(K_HSH)

    def __repr__(self):
        return f"QuiltPackage[{self.attrs}]@{self.local_path()})"

    def __eq__(self, other: QuiltRoot):
        return self.pkg_uri() == other.pkg_uri()

    def path_uri(self, path: str):
        return self.pkg_uri() + "#path=" + path

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

    def open(self):
        return QuiltPackage.OpenLocally(self.dest())

    async def browse(self):
        try:
            q = (
                Package.browse(self.pkg(), top_hash=self.hash)
                if (self.registry().startswith(QuiltID.LOCAL_SCHEME))
                else Package.browse(self.pkg(), self.registry(), top_hash=self.hash)
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

    async def child(self, changed_only=False):
        if changed_only:
            diffs = await self.diff()
            return [x for sub in diffs.values() for x in sub]
        q = await self.remote()
        return list(q.keys())

    async def list(self, changed_only=False):
        return [self.path_uri(k) for k in await self.child(changed_only)]

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
        q.build(self.pkg())
        result = q.push(self.pkg(), registry=self.registry(), message=msg)
        return result

    async def put(self, msg=None):
        """create a new remote revision whether or not package exists / is current"""
        q = await self.remote()
        q.set_dir(".", path=self.dest())
        q.build(self.pkg())
        result = q.push(self.pkg(), registry=self.registry(), message=msg)
        return result

    async def patch(self, msg=None):
        """Update the latest version of the remote package with the staged files"""
        q = await self.remote()
        [q.set(f) for f in self.config.get_stage(adds=True)]
        [q.delete(f) for f in self.config.get_stage(adds=False)]
        q.build(self.pkg())
        print(q)
        result = q.push(self.pkg(), registry=self.registry(), message=msg)
        self.config.update_config({}, reset_stage=True)
        return result

    def delete(self):  # remove local cache
        return shutil.rmtree(self._local_path)

    async def call(self, method: str = "get", msg: str = ""):
        if msg == "":
            msg = f"{QuiltConfig.Now()} {method} {self})"
        attr_method = getattr(self, method)
        return await attr_method(msg) if method[0] == "p" else await attr_method()
