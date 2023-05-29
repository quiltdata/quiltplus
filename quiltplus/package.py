# Resource-oriented version of a Quilt Package

import logging
import shutil

from quilt3 import Package
from pathlib import Path
from typing_extensions import Self

from .uri import QuiltUri
from .local import QuiltLocal

class QuiltPackage(QuiltLocal):
    METHOD_NAMES = "get list diff patch put".split(" ")

    @classmethod
    def FromURI(cls: Self, uri: str):
        attrs = QuiltUri.AttrsFromUri(uri)
        return cls(attrs)

    def __init__(self, attrs: dict):
        super().__init__(attrs)
        self.hash = self.attrs.get(QuiltUri.K_HASH)

    def path_uri(self, sub_path: str):
        return self.pkg_uri() + "#path=" + sub_path

    async def browse(self):
        print(f"browse {self.package} {self.registry} {self.hash}")
        try:
            q = (
                Package.browse(self.package, self.registry, top_hash=self.hash)
            )
            return q
        except Exception as err:
            logging.error(err)
        return None

    async def local_pkg(self):
        q = Package().set_dir(".", path=self.dest())
        return q

    async def remote_pkg(self):
        return await self.browse()

    async def child(self, changed_only=False):
        if changed_only:
            diffs = await self.diff()
            return [x for sub in diffs.values() for x in sub]
        q = await self.remote_pkg()
        return list(q.keys())

    async def list(self, changed_only=False):
        return [self.path_uri(k) for k in await self.child(changed_only)]

    async def diff(self):
        logging.debug(f"\ndiff.local_files\n{self.local_files()}")
        q_remote = await self.remote_pkg()
        logging.debug(f"diff.remote_keys {q_remote.keys()}")
        q_local = await self.local_pkg()
        logging.debug(f"diff.local_keys {q_local.keys()}")
        diffs = q_remote.diff(q_local)
        logging.debug(f"diff: {diffs}")
        return {"added": diffs[0], "modified": diffs[1], "deleted": diffs[2]}
    

    async def get(self, path: Path = None, key=None):

        dest = self.dest()
        q = await self.remote_pkg()
        if key:
            q.fetch(key, dest=dest)
        else:
            q.fetch(dest=dest)
        return dest

    async def post(self, msg=None):  # create new empty package
        q = await self.local_pkg()
        q.build(self.package)
        result = q.push(self.package, registry=self.registry, message=msg)
        return result

    async def put(self, msg=None):
        """create a new remote revision whether or not package exists / is current"""
        q = await self.remote_pkg()
        q.set_dir(".", path=self.dest())
        q.build(self.package)
        result = q.push(self.package, registry=self.registry, message=msg)
        return result

    async def patch(self, msg=None):
        """Update the latest version of the remote package with the staged files"""
        q = await self.remote_pkg()
        [q.set(f) for f in self.config.get_stage(adds=True)]
        [q.delete(f) for f in self.config.get_stage(adds=False)]
        q.build(self.package)
        print(q)
        result = q.push(self.package, registry=self.registry, message=msg)
        return result

    def delete(self):  # remove local cache
        return shutil.rmtree(self.last_path)

    async def call(self, method: str = "get", msg: str = ""):
        if msg == "":
            msg = f"{__class__} {method} {self})"
        attr_method = getattr(self, method)
        return await attr_method(msg) if method[0] == "p" else await attr_method()
