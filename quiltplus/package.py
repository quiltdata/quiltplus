# Resource-oriented version of a Quilt Package

import logging
import shutil
from pathlib import Path

from quilt3 import Package  # type: ignore
from quiltcore import Builder, Changes, Manifest

from .local import QuiltLocal
from .uri import QuiltUri


class QuiltPackage(QuiltLocal):
    ERROR_VOL = "changeset: default volume changed"
    K_STAGE = "stage"
    K_MSG = "message"

    def __init__(self, attrs: dict):
        super().__init__(attrs)
        self.hash = self.attrs.get(QuiltUri.K_HASH)

    #
    # Helper Methods
    #

    def path_uri(self, sub_path: str):
        return self.pkg_uri() + f"&{self.K_PTH}=" + sub_path

    def stage_uri(self, stage: str, sub_path: str):
        return self.path_uri(sub_path).replace(
            self.PREFIX, f"{self.PREFIX}{self.K_STAGE}+{stage}+"
        )

    def local_man(self) -> Manifest:
        try:
            return self.volume.read_manifest(self.hash)  # type: ignore
        except Exception:
            raise ValueError(f"no local manifest for hash: {self.hash}")

    def remote_man(self) -> Manifest:
        tag = self.attrs.get(QuiltUri.K_TAG, self.namespace.TAG_DEFAULT)
        opts = {self.domain.KEY_HSH: self.hash} if self.hash else {}
        print(f"remote_man.pkg: {self.package}:{tag}@{self.hash} -> {opts}")
        man = self.namespace.get(tag, **opts)
        if not isinstance(man, Manifest):
            raise ValueError(f"no remote manifest for hash: {self.hash}")
        return man

    #
    # Retrieval Methods
    #

    async def child(self):
        man = self.remote_man()
        return [entry.name for entry in man.list()]

    async def list(self, opts: dict = {}):
        return [self.path_uri(k) for k in await self.child()]

    async def get(self, opts: dict = {}):
        """Download package to dest"""
        dest = self.check_dir_arg(opts)
        logging.debug(f"get dest={dest}: {opts}")
        man = self.remote_man()
        rc = self.volume.put(man)  # TODO: update self.tag
        files = self.local_files()
        return [f"file://{fn}" for fn in files]
    
    #
    # Create/Revise Package
    #

    def n_changes(self) -> int:
        return len(self.changes.keystore)

    def changeset(self) -> Changes:
        vpath = self.volume.path
        if not hasattr(self, "changes") or self.n_changes() == 0:
            self.changes = Changes(vpath)
        if self.changes.path == vpath:
            return self.changes
        
        raise ValueError(f"{self.ERROR_VOL}: {self.changes.path} != {vpath}")

    def commit(self, **kwargs) -> Manifest:
        """
        Create manifest.
        Store in the local registry.
        """
        src = self.check_dir_arg(kwargs)
        msg = kwargs.get(self.K_MSG, f"{__name__} {self.Now()} @ {kwargs}")
        logging.debug(f"commit[{msg}] src={src}")
        changes = self.changeset()
        if self.n_changes() == 0:
            changes.post(src)
        build = Builder(changes)
        man = build.post(build.path)
        if not isinstance(man, Manifest):
            raise ValueError(f"can not create manifest for {changes}")
        return man

    async def push(self, q: Package, opts: dict):
        """Generic handler for all push methods"""
        dest = self.check_dir_arg(opts)
        kwargs = {
            self.K_REG: self.registry,
            self.K_FORCE: not opts.get(self.K_FAIL, False),
            self.K_MSG: opts.get(
                self.K_MSG, f"{__name__} {self.Now()} @ {opts}"
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

    #
    # Legacy Methods
    #

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
    
    def delete(self):  # remove local cache
        return shutil.rmtree(self.last_path)

    async def call(self, method: str = "get", opts={}):
        attr_method = getattr(self, method)
        return await attr_method(opts)
