from pathlib import Path

from quilt3 import list_packages
from yaml import Loader, dump, load, safe_load

from .id import QuiltID
from .package import QuiltPackage

ROOT = Path.home() / "Documents" / "QuiltData"
RECENTS = "recents.yaml"


class QuiltClient:
    def __init__(self, root=ROOT):
        self.root = root
        self.path = root / RECENTS
        self.path.touch(exist_ok=True)
        print(self.path)
        print(self.path.is_file())

        with self.path.open() as f:
            self.recents = load(f, Loader) or {}

    async def get(self, qid, asType=None):
        type = asType or qid.type()
        try:
            resource = QuiltPackage(qid)  # Should create appropriate resource by type
            self.update(qid)
            return resource
        except Exception as err:
            print(err)
            return None

    async def list(self, registry=None):
        qids = [QuiltID.FromAttrDict(attr) for attr in self.recents.values()]
        return qids

    def update(self, qid):
        print(f"update: {qid.id()}")
        self.recents[qid.id()] = qid.attr
        print(self.path)
        with self.path.open("a+") as f:
            dump(self.recents, f)
