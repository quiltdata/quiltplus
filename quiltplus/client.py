from pathlib import Path

from quilt3 import list_packages
from yaml import Loader, dump, load, safe_load

from .id import QuiltID
from .package import QuiltPackage

ROOT = Path.home() / "Documents" / "QuiltData"
RECENTS = "recents.yaml"

# get() returns recent QuiltID by numerical index
# get(index) returns Package with that index
# delete(index) removes QuiltID with that index from recents
# put(index) updates Package with that index
# post() create Package (add to recents)


class QidCache:
    def __init__(self, path):
        self.path = path
        self.path.touch(exist_ok=True)
        self.qids = set()
        self.load_qids()
        self.saved = False
        print(f"QidCache.load_qids[{path}] {len(self.qids)}")

    def save_qids(self):
        recents = [qid.attrs for qid in self.qids]
        print(f"QidCache.save_qids[{self.path}] {self.size()} / {len(recents)}")
        with self.path.open("w+") as f:
            dump(recents, f)
        self.saved = True

    def load_qids(self):
        with self.path.open() as f:
            recents = load(f, Loader) or []
            print("load_qids.recents", recents)
            {self.create_qid(attrs) for attrs in recents}

    def find_qid(self, index):
        result = [q for q in self.qids if q.index == index]
        return next(iter(result), None)

    def add_qid(self, qid):
        self.qids.add(qid)

    def create_qid(self, attrs):
        qid = QuiltID.FromAttrs(attrs)
        qid.client = self
        self.add_qid(qid)
        return qid

    def remove_qid(self, index):
        qid = self.find_qid(index)
        if qid:
            self.qids.remove(qid)
            return qid

    def size(self):
        return len(self.qids)

    def __del__(self):
        assert (
            self.saved or self.path.exists()
        ), f"Cannot save QidCache[{self.path}]saved={self.saved}"
        if self.path.exists():
            self.save_qids()


class QuiltClient(QidCache):
    def __init__(self, root=ROOT):
        root.mkdir(parents=True, exist_ok=True)
        super().__init__(root / RECENTS)
        self.root = root

    async def delete(self, index):
        return self.remove_qid(index)

    async def post(self, attrs):
        return self.create_qid(attrs)

    async def put(self, attrs, index):
        print("put.size", self.size())
        await self.delete(index)
        print("put.delete.size", self.size())
        qid = QuiltID.FromAttrs(attrs, index)
        print("put.FromAttrs.size", self.size())
        self.add_qid(qid)
        print("put.add_qid.size", self.size())
        return qid

    async def get(self, index=-1):
        if index < 1:
            return list(self.qids)
        try:
            qid = self.find_qid(index)
            # resource = QuiltPackage(qid)
            return qid
        except Exception as err:
            print(err)
            return None
