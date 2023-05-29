# Create Immutable Identifier from a Quilt+ URI
from urllib.parse import parse_qs, urlparse

PREFIX = "quilt+"
SEP = "+"
K_HOST = "_hostname"
K_PROT = "_protocol"
K_QRY = "_query"
K_TOOL = "_tool"
K_URI = "_uri"
K_ID = "_id"

SEP_HASH = "@"
SEP_TAG = ":"

K_PID = "local_path"
K_STR = "storage"
K_HSH = "top_hash"
K_BKT = "bucket"
K_PKG = "package"
K_PKG_NAME = "package_name"
K_PTH = "path"
K_PRP = "property"
K_TAG = "tag"
K_VER = "versions"
K_CAT = "catalog"


K_PKG_FULL = "__package__"
K_STR_DEFAULT = "s3"
FRAG_KEYS = [K_PKG_FULL, K_PTH, K_PRP, K_CAT]


class QuiltParse:
    def __init__(self, uri_string):
        self.uri = urlparse(uri_string)
        if not self.uri:
            raise ValueError(f"Error: invalid URI: {uri_string}")
        self.attrs = self.parse_fragments(self.uri.fragment)
        self.attrs[K_STR] = self.parse_prefix(self.uri.scheme)
        self.attrs[K_BKT] = self.uri.netloc
        self._type = self.parse_type()
        self.parse_scheme(self.uri.scheme)
        self.attrs[K_HOST] = self.uri.hostname
        self.attrs[K_QRY] = self.uri.query
        self.attrs[K_URI] = uri_string

    def __str__(self):
        return self.__repr__()

    def get(self, key):
        return self.attrs.get(key)

    def parse_fragments(self, fragment):
        list_dict = parse_qs(fragment)
        scalars = {k: v[0] for k, v in list_dict.items()}
        return scalars
    
    def parse_prefix(self, uri):
        if not uri.startswith(PREFIX):
            raise ValueError(f"Error: invalid URI prefix: {uri}")
        return uri.replace(PREFIX, "")

    def parse_scheme(self, scheme: str):
        schemes = scheme.split(SEP)
        if len(schemes) != 2:
            raise ValueError(
                f"Error: URI scheme `{self.uri.scheme}` does not contain '{SEP}'"
            )
        self.attrs[K_TOOL] = schemes[0]
        self.attrs[K_PROT] = schemes[1]

    def parse_type(self):
        self.has_package = self.parse_package()
        if K_PRP in self.attrs:
            return K_PRP
        elif K_PTH in self.attrs:
            return K_PTH
        elif K_PKG in self.attrs:
            return K_PKG
        return K_BKT

    def parse_package(self):
        if K_PKG not in self.attrs:
            return False
        pkg = self.attrs[K_PKG]
        self._type = K_VER
        if SEP_HASH in pkg:
            self._type = K_PKG
            s = pkg.split("@")
            self.attrs[K_HSH] = s[1]
            self.attrs[K_PKG] = s[0]
        if SEP_TAG in pkg:
            self._type = K_PKG
            s = pkg.split(":")
            self.attrs[K_TAG] = s[1]
            self.attrs[K_PKG] = s[0]
        return True
