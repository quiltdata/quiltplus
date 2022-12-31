# Create Immutable Identifier from a Quilt+ URI

from pathlib import Path
from urllib.parse import parse_qs, urlparse

K_CLD = "cloud"
K_HSH = "top_hash"
K_HNM = "hostname"
K_ID = "id"
K_PID = "id_path"
K_PKG = "package"
K_PTH = "path"
K_PRP = "property"
K_REG = "registry"
K_QRY = "query"
K_TAG = "tag"

PREFIX = "quilt+"
TYPES = [K_CLD, K_REG, K_PTH, K_PRP, K_QRY, None]


class QuiltID:
    def __init__(self, uri_string):
        self.raw = uri_string
        self.uri = urlparse(uri_string)
        self.attr = self.parse_fragments(self.uri.fragment)
        self.parse_id(self.uri.netloc)
        self.attr[K_QRY] = self.uri.query

    def get(self, key):
        return self.attr[key]

    def id(self):
        return self.get(K_ID)

    def type(self):
        for index, key in enumerate(TYPES):
            next_key = TYPES[index + 1]
            if next_key not in self.attr:
                return key
        return False

    def parse_fragments(self, fragment):
        list_dict = parse_qs(fragment)
        scalars = {k: v[0] for k, v in list_dict.items()}
        return scalars

    def parse_id(self, host):
        if not PREFIX in self.uri.scheme:
            raise ValueError(f"Error: invalid URI scheme {self.uri.scheme}: {self.uri}")
        self.attr[K_CLD] = self.uri.scheme.replace(PREFIX, "")
        self.attr[K_HNM] = host
        self.attr[K_REG] = f"{self.attr[K_CLD]}://{host}"
        self.attr[K_PID] = Path(self.attr[K_CLD]) / host
        if self.parse_package():
            self.attr[K_PID] /= self.attr[K_PKG]
        self.attr[K_ID] = str(self.attr[K_PID])

    def parse_package(self):
        if K_PKG not in self.attr:
            return False
        pkg = self.attr[K_PKG]
        if "@" in pkg:
            s = pkg.split("@")
            self.attr[K_HSH] = s[1]
            self.attr[K_PKG] = s[0]
        if ":" in pkg:
            s = pkg.split(":")
            self.attr[K_TAG] = s[1]
            self.attr[K_PKG] = s[0]
        return True
