from pathlib import Path

from yaml import safe_load

ROOT = Path.home() / "Documents" / "QuiltData"
RECENTS = "recents.yaml"


class QuiltClient:
    def __init__(self, root=ROOT):
        self.root = root
        self.file = root / RECENTS
        self.recents = safe_load(self.file)

    def get(self):
        return self.root

    def list(self):
        self.recents
