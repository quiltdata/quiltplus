# Create Immutable Identifier from a Quilt+ URI
from urllib.parse import parse_qs, urlparse

PREFIX = "quilt+"

K_PID = "local_path"
K_STR = "storage"
K_HSH = "top_hash"
K_BKT = "bucket"
K_PKG = "package"
K_PTH = "path"
K_PRP = "property"
K_QRY = "query"
K_TAG = "tag"
K_CAT = "catalog"

K_PKG_FULL = "__package__"
K_STR_DEFAULT = "s3"
TYPES = [K_STR, K_BKT, K_PKG, K_CAT, K_PTH, K_PRP, K_QRY, None]
FRAG_KEYS = [K_PKG_FULL, K_PTH, K_PRP, K_CAT]


class QuiltParse:
    def __init__(self, uri_string):
        self.uri = urlparse(uri_string)
        self.attrs = self.parse_fragments(self.uri.fragment)
        self.parse_id(self.uri.netloc)
        self.attrs[K_QRY] = self.uri.query

    def __str__(self):
        return self.__repr__()

    def get(self, key):
        return self.attrs.get(key)

    def parse_fragments(self, fragment):
        list_dict = parse_qs(fragment)
        scalars = {k: v[0] for k, v in list_dict.items()}
        return scalars

    def parse_id(self, host):
        if PREFIX not in self.uri.scheme:
            raise ValueError(f"Error: invalid URI scheme {self.uri.scheme}: {self.uri}")
        self.attrs[K_STR] = self.uri.scheme.replace(PREFIX, "")
        self.attrs[K_BKT] = host
        self.has_package = self.parse_package()

    def parse_package(self):
        if K_PKG not in self.attrs:
            return False
        pkg = self.attrs[K_PKG]
        if "@" in pkg:
            s = pkg.split("@")
            self.attrs[K_HSH] = s[1]
            self.attrs[K_PKG] = s[0]
        if ":" in pkg:
            s = pkg.split(":")
            self.attrs[K_TAG] = s[1]
            self.attrs[K_PKG] = s[0]
        return True
