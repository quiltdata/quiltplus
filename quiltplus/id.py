# Create Immutable Identifier from a Quilt+ URI

from pathlib import Path
from socket import gethostname
from urllib.parse import parse_qs, urlparse

from .unparse import *


class QuiltID:

    LOCAL_HOST = gethostname()
    LOCAL_SCHEME = "local"
    INDEX = 0

    @classmethod
    def Decode(cls, encoded):
        decoded = encoded.replace("%2F", "/").replace("%40", "@")
        return decoded

    @classmethod
    def FromAttrs(cls, attrs, index=None):
        uri_string = QuiltUnparse(attrs).unparse()
        return cls(uri_string, index)

    @classmethod
    def Local(cls, pkg):
        uri_string = (
            f"{PREFIX}{QuiltID.LOCAL_SCHEME}://{QuiltID.LOCAL_HOST}#package={pkg}"
        )
        return cls(uri_string)

    def __init__(self, uri_string, index=None):
        self.uri = urlparse(uri_string)
        self.attrs = self.parse_fragments(self.uri.fragment)
        self.parse_id(self.uri.netloc)
        self.attrs[K_QRY] = self.uri.query
        self.attrs[K_RAW] = uri_string
        if index:
            self.index = index
        else:
            QuiltID.INDEX += 1
            self.index = QuiltID.INDEX

    def get(self, key):
        return self.attrs.get(key)

    def id(self):
        return self.get(K_ID)

    def source(self):
        return self.get(K_RAW)

    def type(self):
        for index, key in enumerate(TYPES):
            next_key = TYPES[index + 1]
            if next_key not in self.attrs:
                return key
        return False

    def parse_fragments(self, fragment):
        list_dict = parse_qs(fragment)
        scalars = {k: v[0] for k, v in list_dict.items()}
        return scalars

    def parse_id(self, host):
        if not PREFIX in self.uri.scheme:
            raise ValueError(f"Error: invalid URI scheme {self.uri.scheme}: {self.uri}")
        self.attrs[K_STR] = self.uri.scheme.replace(PREFIX, "")
        self.attrs[K_HNM] = host
        self.attrs[K_REG] = f"{self.attrs[K_STR]}://{host}"
        self.attrs[K_PID] = Path(self.attrs[K_STR]) / host
        if self.parse_package():
            self.attrs[K_PID] /= self.attrs[K_PKG]
        self.attrs[K_ID] = str(self.attrs[K_PID])

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
