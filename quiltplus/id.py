# Create Immutable Identifier from a Quilt+ URI

from pathlib import Path
from socket import gethostname
from urllib.parse import parse_qs, urlparse

K_RAW = "source_uri"
K_STR = "store"
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
TYPES = [K_STR, K_REG, K_PTH, K_PRP, K_QRY, None]


class QuiltID:
    LOCAL_HOST = gethostname()
    LOCAL_SCHEME = "local"

    @classmethod
    def FromAttrDict(cls, attr):
        uri_string = attr[K_RAW]
        return cls(uri_string)

    @classmethod
    def Local(cls, pkg):
        uri_string = (
            f"{PREFIX}{QuiltID.LOCAL_SCHEME}://{QuiltID.LOCAL_HOST}#package={pkg}"
        )
        return cls(uri_string)

    def __init__(self, uri_string):
        self.uri = urlparse(uri_string)
        self.attr = self.parse_fragments(self.uri.fragment)
        self.parse_id(self.uri.netloc)
        self.attr[K_QRY] = self.uri.query
        self.attr[K_RAW] = uri_string

    def get(self, key):
        return self.attr[key]

    def id(self):
        return self.get(K_ID)

    def source(self):
        return self.get(K_RAW)

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
        self.attr[K_STR] = self.uri.scheme.replace(PREFIX, "")
        self.attr[K_HNM] = host
        self.attr[K_REG] = f"{self.attr[K_STR]}://{host}"
        self.attr[K_PID] = Path(self.attr[K_STR]) / host
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
