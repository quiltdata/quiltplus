# Create Immutable Identifier from a Quilt+ URI
import logging
from pathlib import Path
from socket import gethostname
from urllib.parse import parse_qs, urlparse

from .unparse import *


class QuiltID:

    LOCAL_HOST = gethostname()
    LOCAL_SCHEME = "local"
    INDEX = 0

    @classmethod
    def FromAttrs(cls, attrs, index=None):
        if K_STR not in attrs:
            attrs[K_STR] = K_STR_DEFAULT
        uri_string = QuiltUnparse(attrs).unparse()
        logging.debug(f"FromAttrs: {uri_string}", attrs)
        return cls(uri_string, index)

    @classmethod
    def Local(cls, pkg):
        uri_string = (
            f"{PREFIX}{QuiltID.LOCAL_SCHEME}://{QuiltID.LOCAL_HOST}#package={pkg}"
        )
        return cls(uri_string)

    def __init__(self, uri_string, index=None):
        self.cache = None
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

    def __repr__(self):
        return f"QuiltID({self.quilt_uri()}, {self.index})"

    def __str__(self):
        return self.__repr__()

    def get(self, key):
        return self.attrs.get(key)

    def id(self):
        return self.get(K_ID)

    def local(self):
        return str(self.cache.root / self.id()) if self.cache else None

    def registry(self):
        return f"{self.get(K_STR)}://{self.get(K_BKT)}"

    def source(self):
        return self.get(K_RAW)

    def quilt_uri(self):
        uri_string = QuiltUnparse(self.attrs).unparse()
        return uri_string

    def with_keys(self, index, title, subtitle):
        return {
            index: self.index,
            title: self.get(K_PKG),
            subtitle: self.source(),
        }

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
        self.attrs[K_BKT] = host
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
