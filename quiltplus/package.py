# Resource-oriented version of a Quilt Package

import logging
import shutil
from pathlib import Path

from quilt3 import Package
from typing_extensions import Self

from .local import QuiltLocal
from .uri import QuiltUri


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
        return self.pkg_uri() + "&path=" + sub_path

    async def browse(self):
        logging.debug(f"browse {self.package} {self.registry} {self.hash}")
        try:
            q = Package.browse(self.package, self.registry, top_hash=self.hash)
            return q
        except Exception as err:
            logging.error(err)
        return None

    async def local_pkg(self):
        q = Package().set_dir(".", path=self.dest())
        return q

    async def remote_pkg(self):
        return (await self.browse()) or Package()

    async def child(self, changed_only=False):
        if changed_only:
            diffs = await self.diff()
            return [x for sub in diffs.values() for x in sub]
        q = await self.remote_pkg()
        return list(q.keys())

    async def list(self, opts: dict = {}):
        return [self.path_uri(k) for k in await self.child()]

    async def diff(self):
        logging.debug(f"\ndiff.local_files\n{self.local_files()}")
        q_remote = await self.remote_pkg()
        logging.debug(f"diff.remote_keys {q_remote.keys()}")
        q_local = await self.local_pkg()
        logging.debug(f"diff.local_keys {q_local.keys()}")
        diffs = q_remote.diff(q_local)
        logging.debug(f"diff: {diffs}")
        return {"added": diffs[0], "modified": diffs[1], "deleted": diffs[2]}

    def check_path(self, opts: dict):
        if QuiltUri.K_PTH in opts:
            self.check_dir(opts[QuiltUri.K_PTH])
        return self.dest()
    
    async def get(self, opts: dict = {}):
        dest = self.check_path(opts)
        q = await self.remote_pkg()
        q.fetch(dest=dest)
        return dest
    
    async def push_args(self, opts: dict) -> dict:
        kwargs = {
            "registry": self.registry,
            "force": opts.get("force", False),
            "message": opts.get("message", f"{__name__} {QuiltUri.Now()} @ {opts}"),
        }
        if "commit" in opts:
            await self.commit(opts)
        return kwargs

    async def commit(self, opts: dict = {}):  # create new empty package
        q = await self.local_pkg()
        [q.set(f) for f in self.config.get_stage(adds=True)]
        [q.delete(f) for f in self.config.get_stage(adds=False)]
        result = q.build(self.package)
        return result

    async def push(self, opts: dict, put = True):
        """Generic handler for all push methods"""
        q = await self.remote_pkg() # reset to latest
        if put:
            [q.delete(f) for f in await self.child()] # clean slate; replace with dest
        q.set_dir(".", self.check_path(opts))
        q.build(self.package)
        args = await self.push_args(opts)
        result = q.push(self.package, **args)
        return result

    async def put(self, opts: dict = {}):
        return await self.push(opts, put = True)

    async def patch(self, opts: dict = {}):
        """Update the latest version of the remote package with the latest commit"""
        return await self.push(opts, put = False)

    def delete(self):  # remove local cache
        return shutil.rmtree(self.last_path)

    async def call(self, method: str = "get", opts = {}):
        attr_method = getattr(self, method)
        return await attr_method(opts)
