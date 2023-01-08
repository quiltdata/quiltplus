from urllib.parse import urlencode, urlunparse

PREFIX = "quilt+"

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

TYPES = [K_STR, K_REG, K_PKG, K_PTH, K_PRP, K_QRY, None]
FRAG_KEYS = [K_PKG, K_PTH, K_PRP]


class QuiltUnparse:
    def __init__(self, attrs):
        self.attrs = attrs
        self.pkg = self.get(K_PKG)
        self.unparse_package()

    def get(self, key):
        return self.attrs.get(key)

    def unparse_package(self):
        if K_HSH in self.attrs:
            self.attrs[K_PKG] = f"{self.pkg}@{self.get(K_HSH)}"
        elif K_TAG in self.attrs:
            self.attrs[K_PKG] = f"{self.pkg}:{self.get(K_TAG)}"

    def unparse_fragments(self):
        frags = {k: self.get(k) for k in FRAG_KEYS if self.get(k)}
        return urlencode(frags)

    # (scheme='', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html', params='', query='', fragment='')
    def unparse(self):
        args = (
            PREFIX + self.get(K_STR),
            self.get(K_HNM),
            "",
            "",
            self.get(K_QRY),
            self.unparse_fragments(),
        )
        return urlunparse(args)
