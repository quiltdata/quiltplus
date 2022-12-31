from pathlib import Path

from yaml import Loader, dump, load, safe_load

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

    def get(self, qid, asType=None):
        type = asType or qid.type()
        resource = QuiltPackage(qid)  # Should create appropriate resource by type
        self.update(qid)
        return resource

    def list(self):
        return self.recents

    def update(self, qid):
        self.recents[qid.raw] = qid.attr
        print(self.path)
        with self.path.open("a+") as f:
            dump(self.recents, f)
