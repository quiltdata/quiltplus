# Create URL from attributes
from urllib.parse import urlencode, urlunparse

from .parse import (
    FRAG_KEYS,
    K_BKT,
    K_HSH,
    K_PKG,
    K_PKG_FULL,
    K_QRY,
    K_STR,
    K_TAG,
    PREFIX,
)


class QuiltUnparse:
    @classmethod
    def Decode(cls, encoded):
        decoded = encoded.replace("%2F", "/").replace("%40", "@")
        return decoded

    def __init__(self, attrs):
        self.attrs = attrs
        self.attrs[K_PKG_FULL] = self.get(K_PKG)
        self.unparse_package()

    def get(self, key):
        return self.attrs.get(key)

    def has(self, key):
        return key in self.attrs and len(self.get(key)) > 0

    def unparse_package(self):
        if self.has(K_HSH):
            self.attrs[K_PKG_FULL] = f"{self.get(K_PKG)}@{self.get(K_HSH)}"
        elif self.has(K_TAG):
            self.attrs[K_PKG_FULL] = f"{self.get(K_PKG)}:{self.get(K_TAG)}"

    def unparse_fragments(self):
        frags = {k: self.get(k) for k in FRAG_KEYS if self.get(k)}
        encoded = urlencode(frags)
        return encoded.replace(K_PKG_FULL, K_PKG)

    def unparse(self):
        args = (
            PREFIX + self.get(K_STR),
            self.get(K_BKT),
            "",
            "",
            self.get(K_QRY),
            self.unparse_fragments(),
        )
        encoded = urlunparse(args)
        return QuiltUnparse.Decode(encoded)
