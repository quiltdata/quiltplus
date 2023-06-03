# Resource-oriented version of a Quilt Package

import logging
import shutil

from quilt3 import Package  # type: ignore
from typing_extensions import Self, Type

from .local import QuiltLocal
from .uri import QuiltUri


class QuiltPackage(QuiltLocal):
    METHOD_NAMES = "get list diff patch put".split(" ")

    @classmethod
    def FromURI(cls: Type[Self], uri: str):
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

    async def diff(self, opts: dict = {}):
        logging.debug(f"\ndiff.local_files\n{self.local_files()}")
        q_remote = await self.remote_pkg()
        logging.debug(f"diff.remote_keys {q_remote.keys()}")
        q_local = await self.local_pkg()
        logging.debug(f"diff.local_keys {q_local.keys()}")
        diffs = q_remote.diff(q_local)
        logging.debug(f"diff: {diffs}")
        return {"added": diffs[0], "modified": diffs[1], "deleted": diffs[2]}

    async def get(self, opts: dict = {}):
        dest = self.check_path(opts)
        q = await self.remote_pkg()
        q.fetch(dest=dest)
        return dest

    async def commit(self, opts: dict = {}):  # create new empty package
        pass

    async def push(self, q: Package, opts: dict):
        """Generic handler for all push methods"""
        kwargs = {
            "registry": self.registry,
            "force": True,
            "message": opts.get("message", f"{__name__} {QuiltUri.Now()} @ {opts}"),
        }
        q.set_dir(".", self.check_path(opts))
        q.build(self.package)
        result = q.push(self.package, **kwargs)
        return result

    async def put(self, opts: dict = {}):
        q = Package()
        return await self.push(q, opts)

    async def patch(self, opts: dict = {}):
        """Use contents of directory to (merge) update the remote package"""
        q = await self.remote_pkg()  # reset to latest
        return await self.push(q, opts)

    def delete(self):  # remove local cache
        return shutil.rmtree(self.last_path)

    async def call(self, method: str = "get", opts={}):
        attr_method = getattr(self, method)
        return await attr_method(opts)
