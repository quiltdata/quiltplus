# Resource-oriented version of a Quilt Package

import logging
import shutil

from quilt3 import Package  # type: ignore
from typing_extensions import Self, Type, Coroutine

from .local import QuiltLocal
from .uri import QuiltUri


class QuiltPackage(QuiltLocal):
    K_STAGE = "stage"
    K_MSG = "message"
    ERR_MOD = "Local files have been modifie. Use --force to overwrite."

    @classmethod
    def FromURI(cls: Type[Self], uri: str):
        attrs = QuiltUri.AttrsFromUri(uri)
        return cls(attrs)

    def __init__(self, attrs: dict):
        super().__init__(attrs)
        self.hash = self.attrs.get(QuiltUri.K_HASH)

    def path_uri(self, sub_path: str):
        return self.pkg_uri() + f"&{QuiltPackage.K_PTH}=" + sub_path

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

    async def child(self):
        q = await self.remote_pkg()
        return list(q.keys())

    async def list(self, opts: dict = {}):
        return [self.path_uri(k) for k in await self.child()]
    
    def stage_uri(self, stage: str, sub_path: str):
        return self.path_uri(sub_path).replace(
            QuiltPackage.PREFIX,
            f"{QuiltPackage.PREFIX}{QuiltPackage.K_STAGE}+{stage}"
        )

    async def diff(self, opts: dict = {}):
        """List files that differ from local_cache()"""
        self.check_dir
        diffs = self._diff()
        return [self.stage_uri(stage, filename) for filename, stage in diffs.items()]
    
    def unexpected_loss(self, opts: dict = {}) -> bool:
        """Check if _diff and not force"""
        modified = len(self._diff()) > 0
        force = opts.get(QuiltPackage.K_FORCE, False)
        return modified and not force

    async def get(self, opts: dict = {}):
        """Download package to dest()"""
        dest = self.check_path(opts)
        if self.unexpected_loss(opts):
            raise ValueError(f"{QuiltPackage.ERR_MOD}\n{self._diff()}")
        q = await self.remote_pkg()
        q.fetch(dest=dest)
        return self.local_files()

    async def commit(self, opts: dict = {}):
        """Create package in the local registry"""
        pass

    async def push(self, q: Package, opts: dict):
        """Generic handler for all push methods"""
        kwargs = {
            "registry": self.registry,
            QuiltPackage.K_FORCE: True,
            QuiltPackage.K_MSG: opts.get(
                QuiltPackage.K_MSG, 
                f"{__name__} {QuiltPackage.Now()} @ {opts}"
            ),
        }
        q.set_dir(".", self.check_path(opts))
        q.build(self.package)
        result = q.push(self.package, **kwargs)
        return [self.uri]

    async def put(self, opts: dict = {}):
        """Create a new remote version that exactly matches the local folder"""
        q = Package()
        return await self.push(q, opts)

    # TODO: fail if remote package is newer (unless --force)
    async def patch(self, opts: dict = {}):
        """Use contents of directory to (merge) update the remote package"""
        q = await self.remote_pkg()  # reset to latest
        return await self.push(q, opts)

    def delete(self):  # remove local cache
        return shutil.rmtree(self.last_path)

    async def call(self, method: str = "get", opts={}):
        attr_method = getattr(self, method)
        return await attr_method(opts)
