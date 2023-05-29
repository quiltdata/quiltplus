# Create Quilt URI from UnURI attributes

from typing_extensions import Self

from udc import K_HOST, K_PROT, K_URI, UnUri

from .type import QuiltType


class QuiltUri(QuiltType):

    @staticmethod
    def FromUnUri(un: UnUri) -> Self:
        return QuiltUri(un.attrs)

    @staticmethod
    def FromUri(uri: str) -> Self:
        un = UnUri(uri)
        return QuiltUri.FromUnUri(un)

    @staticmethod
    def AttrsFromUri(uri: str) -> dict:
        un = UnUri(uri)
        return un.attrs

    def __init__(self, attrs: dict):
        self.attrs = attrs
        self.uri = attrs.get(K_URI)
        self.registry = f"{attrs.get(K_PROT)}://{attrs.get(K_HOST)}"
        self.package = self.parse_package()

    def __repr__(self):
        return f"QuiltUri({self.uri})"

    def __eq__(self, other: Self):
        return self.registry == other.registry and self.package == other.package and self.__class__ == other.__class__

    #def get(self, key): return self.attrs.get(key)

    def full_package(self):
        return self.attrs.get(QuiltUri.K_PKG)

    def split_package(self, key):
        pkg = self.full_package()
        if not pkg or not key in pkg:
            return None
        s = pkg.split(key)
        self.attrs[key] = s[1]
        return s[0]

    def parse_package(self):
        return self.split_package(QuiltUri.SEP_HASH) or self.split_package(QuiltUri.SEP_TAG) or self.full_package()
