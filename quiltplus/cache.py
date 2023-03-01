# Client managing local package cache (pseudo-registry)

# get() returns recent QuiltID by numerical index
# get(index) returns Package with that index
# delete(index) removes QuiltID with that index from recents
# put(index) updates Package with that index
# post() create Package (add to recents)

# TODO: Make this explicitly Local, and support Remote registries

import logging
from pathlib import Path

from yaml import Loader, dump, load

from .id import QuiltID

ROOT = Path.home() / "Documents" / "QuiltData"
RECENTS = "recents.yaml"


class IdCache:
    def __init__(self, path):
        self.cache_file = path
        self.cache_file.touch(exist_ok=True)
        self.qids = set()
        self.load_qids()
        self.dirty = False
        logging.debug(f"{__class__.__name__}.load_qids[{path}] {len(self.qids)}")

    def save_qids(self):
        recents = [qid.attrs for qid in self.qids]
        name = f"{__class__.__name__}.save_qids[{self.cache_file}]"
        logging.debug(f"{name} {self.size()} / {len(recents)}")
        with self.cache_file.open("w+") as f:
            dump(recents, f)
        self.dirty = False

    def load_qids(self):
        with self.cache_file.open() as f:
            recents = load(f, Loader) or []
            logging.debug("load_qids.recents: {recents}")
            {self.create_qid(attrs) for attrs in recents}

    def find_qid(self, index):
        result = [q for q in self.qids if q.index == index]
        return next(iter(result), None)

    def add_qid(self, qid):
        self.dirty = True
        self.qids.add(qid)

    def create_qid(self, attrs):
        qid = QuiltID.FromAttrs(attrs)
        qid.cache = self
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
            not self.dirty or self.cache_file.exists()
        ), f"Cannot save {__class__.__name__}[{self.cache_file}]saved={self.saved}"
        if self.cache_file.exists():
            print(f"{__class__.__name__}.__del__[{self.cache_file}]")
            self.save_qids()


class QuiltIdCache(IdCache):
    def __init__(self, root=ROOT):
        root.mkdir(parents=True, exist_ok=True)
        super().__init__(root / RECENTS)
        self.root = root

    def __repr__(self):
        return f"{__class__.__name__}({self.root})"

    def __str__(self):
        return self.__repr__()

    async def delete(self, index):
        return self.remove_qid(index)

    async def post(self, attrs):
        return self.create_qid(attrs)

    async def put(self, attrs, index):
        logging.debug(f"put.size: {self.size()}")
        await self.delete(index)
        logging.debug(f"put.delete.size: {self.size()}")
        qid = QuiltID.FromAttrs(attrs, index)
        self.add_qid(qid)
        return qid

    async def get(self, index=-1):
        if index < 1:
            return list(self.qids)
        try:
            qid = self.find_qid(index)
            # resource = QuiltPackage(qid)
            return qid
        except Exception as err:
            logging.error(err)
            return None
