# Resource-oriented version of a Quilt Package

import logging
import shutil

from quilt3 import Package  # type: ignore

from .local import QuiltLocal
from .uri import QuiltUri


class QuiltPackage(QuiltLocal):
    K_STAGE = "stage"
    K_MSG = "message"
    ERR_MOD = (
        f"Local files have been modified. Unset --{QuiltLocal.K_FAIL} to overwrite."
    )

    def __init__(self, attrs: dict):
        super().__init__(attrs)
        self.hash = self.attrs.get(QuiltUri.K_HASH)

    def path_uri(self, sub_path: str):
        return self.pkg_uri() + f"&{QuiltPackage.K_PTH}=" + sub_path

    async def browse(self):
        logging.debug(f"browse {self.package} {self.registry} {self.hash}")
        try:
            q = (
                Package.browse(self.package, self.registry, top_hash=self.hash)
                if self.hash
                else Package.browse(self.package, self.registry)
            )
            return q
        except Exception as err:
            logging.error(err)
        return None

    async def local_pkg(self):
        q = Package().set_dir(".", path=self.dest())
        return q

    async def remote_pkg(self):
        return (await self.browse()) or Package()

    def local_man(self):
        try:
            return self.volume.read_manifest(self.hash)  # type: ignore
        except Exception as err:
            logging.debug(f"no local manifest for hash: {self.hash}")
        return None
    
    def remote_man(self):
        print(f"remote_man: {self.hash} for {self.package} {self.registry}")
        tag = self.attrs.get(QuiltUri.K_TAG, self.namespace.TAG_DEFAULT)
        opts = {QuiltUri.K_HASH: self.hash} if self.hash else {}
        return self.namespace.get(tag, **opts)

    async def child(self):
        q = await self.remote_pkg()
        return list(q.keys())

    async def list(self, opts: dict = {}):
        return [self.path_uri(k) for k in await self.child()]

    def stage_uri(self, stage: str, sub_path: str):
        return self.path_uri(sub_path).replace(
            QuiltPackage.PREFIX, f"{QuiltPackage.PREFIX}{QuiltPackage.K_STAGE}+{stage}+"
        )

    async def diff(self, opts: dict = {}):
        """List files that differ from local_cache()"""
        self.check_dir_arg(opts)
        diffs = self._diff()
        return [self.stage_uri(stage, filename) for filename, stage in diffs.items()]

    def unexpected_loss(self, opts, get=True) -> bool:
        """Check if _diff and fallible"""
        modified = [k for k, v in self._diff().items() if v == "touch"]
        fallible = opts.get(QuiltPackage.K_FAIL, False)
        return len(modified) > 0 and fallible

    async def get(self, opts: dict = {}):
        """Download package to dest()"""
        dest = self.check_dir_arg(opts)
        logging.debug(f"get dest={dest}: {opts}")
        if self.unexpected_loss(opts):
            raise ValueError(f"{dest}: {QuiltPackage.ERR_MOD}\n{self._diff()}")
        q = await self.remote_pkg()
        q.fetch(dest=dest)
        files = self.local_files()
        return [f"file://{fn}" for fn in files]

    async def commit(self, opts: dict = {}):
        """Create package in the local registry"""
        pass

    async def push(self, q: Package, opts: dict):
        """Generic handler for all push methods"""
        dest = self.check_dir_arg(opts)
        kwargs = {
            QuiltPackage.K_REG: self.registry,
            QuiltPackage.K_FORCE: not opts.get(QuiltPackage.K_FAIL, False),
            QuiltPackage.K_MSG: opts.get(
                QuiltPackage.K_MSG, f"{__name__} {QuiltPackage.Now()} @ {opts}"
            ),
        }
        logging.debug(f"push dest={dest}: {opts}\n{kwargs}")
        q.set_dir(".", dest)
        q.build(self.package)
        q.push(self.package, **kwargs)
        self.hash = None  # TODO: get, and return URI with, new hash
        await self.browse()  # reset local registry to latest
        return [self.uri]

    async def put(self, opts: dict = {}):
        """Create a new remote version that exactly matches the local folder"""
        q = Package()
        return await self.push(q, opts)

    # TODO: fail if remote package is newer AND --fallible
    async def patch(self, opts: dict = {}):
        """Use contents of directory to (merge) update the remote package"""
        q = await self.remote_pkg()  # reset to latest
        return await self.push(q, opts)

    def delete(self):  # remove local cache
        return shutil.rmtree(self.last_path)

    async def call(self, method: str = "get", opts={}):
        attr_method = getattr(self, method)
        return await attr_method(opts)
