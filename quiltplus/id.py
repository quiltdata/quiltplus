# Create Immutable Identifier from a Quilt+ URI
import logging
from pathlib import Path
from socket import gethostname
from urllib.parse import parse_qs, urlparse

from .parse import *
from .unparse import *


class QuiltID(QuiltParse):
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
        super().__init__(uri_string)
        self._source_uri = uri_string
        self.cache = None

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

    def sub_path(self):
        sub_path = Path(self.get(K_STR)) / self.get(K_BKT)
        if self.has_package:
            return sub_path / self.attrs[K_PKG]
        return sub_path

    def local_path(self):
        return self.cache.root / self.sub_path() if self.cache else None

    def registry(self):
        return f"{self.get(K_STR)}://{self.get(K_BKT)}"

    def source_uri(self):
        return self._source_uri

    def quilt_uri(self):
        uri_string = QuiltUnparse(self.attrs).unparse()
        return uri_string

    def with_keys(self, index, title, subtitle):
        return {
            index: self.index,
            title: self.get(K_PKG),
            subtitle: self.source_uri(),
        }

    def type(self):
        for index, key in enumerate(TYPES):
            next_key = TYPES[index + 1]
            if next_key not in self.attrs:
                return key
        return False
