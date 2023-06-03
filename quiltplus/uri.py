# Create Quilt URI from UnURI attributes

from un_yaml.un_uri import UnUri

from .type import QuiltType


class QuiltUri(QuiltType):
    @classmethod
    def FromUnUri(cls, un: UnUri) -> "QuiltUri":
        return cls(un.attrs)

    @classmethod
    def FromUri(cls, uri: str) -> "QuiltUri":
        un = UnUri(uri)
        return cls.FromUnUri(un)

    @staticmethod
    def AttrsFromUri(uri: str) -> dict:
        un = UnUri(uri)
        return un.attrs

    def __init__(self, attrs: dict):
        self.attrs = attrs
        self.uri = attrs.get(UnUri.K_URI)
        self.registry = f"{attrs.get(UnUri.K_PROT)}://{attrs.get(UnUri.K_HOST)}"
        self.package = self.parse_package()

    def __repr__(self):
        return f"QuiltUri({self.uri})"

    def __eq__(self, other: object):
        if not isinstance(other, QuiltUri):
            return NotImplemented
        return self.registry == other.registry and self.package == other.package

    def full_package(self):
        return self.attrs.get(QuiltUri.K_PKG)

    def split_package(self, key):
        sep = QuiltUri.SEP.get(key)
        pkg = self.full_package()
        if not pkg or sep not in pkg:
            return None
        s = pkg.split(sep)
        self.attrs[key] = s[1]
        return s[0]

    def parse_package(self):
        return (
            self.split_package(QuiltUri.K_HASH)
            or self.split_package(QuiltUri.K_TAG)
            or self.full_package()
        )
