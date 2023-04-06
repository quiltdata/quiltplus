# Create Immutable Identifier from a Quilt+ URI
import logging
from pathlib import Path
from socket import gethostname
from tempfile import TemporaryDirectory

from .parse import K_BKT, K_CAT, K_HSH, K_PKG, K_STR, K_STR_DEFAULT, PREFIX, TYPES, QuiltParse
from .unparse import QuiltUnparse


class QuiltID(QuiltParse):
    DEFAULT_CATALOG = "open.quiltdata.com"
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
        self._tempDir = None
        self._cleanup = False
        if index:
            self.index = index
        else:
            QuiltID.INDEX += 1
            self.index = QuiltID.INDEX

    def __repr__(self):
        return f"QuiltID({self.quilt_uri()}, {self.index})"

    def __str__(self):
        return self.__repr__()

    def get(self, key, default=None):
        return self.attrs.get(key, default)

    def sub_path(self):
        sub_path = Path(self.get(K_STR)) / self.get(K_BKT)
        if self.has_package:
            return sub_path / self.attrs[K_PKG]
        return sub_path

    def root(self):
        if self._tempDir:
            return Path(self._tempDir.name)
        if self.cache:
            return self.cache.root
        self._tempDir = TemporaryDirectory()
        self._cleanup = False  # "PYTEST_CURRENT_TEST" not in os.environ
        return Path(self._tempDir.name)

    def local_path(self):
        return self.root() / self.sub_path()

    def pkg(self):
        return self.get(K_PKG)

    def hash(self):
        return self.get(K_HSH)

    def registry(self):
        return f"{self.get(K_STR)}://{self.get(K_BKT)}"

    def source_uri(self):
        return self._source_uri

    def quilt_uri(self):
        uri_string = QuiltUnparse(self.attrs).unparse()
        return uri_string

    def catalog_uri(self):
        catalog = self.get(K_CAT, QuiltID.DEFAULT_CATALOG)
        uri_string = f"https://{catalog}/b/{self.get(K_BKT)}"
        if self.has_package:
            uri_string += f"/packages/{self.get(K_PKG)}"
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

    def __del__(self):
        if self._cleanup:
            print(f"{__class__.__name__}.__del__[{self._tempDir}]")
            self._tempDir.cleanup()
