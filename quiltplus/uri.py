# Create Quilt URI from UnURI attributes

from un_yaml import UnUri  # type: ignore

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
        package = self.parse_package()
        self.package: str = package if isinstance(package, str) else ""

    def __repr__(self):
        return f"QuiltUri({self.uri})"

    def __eq__(self, other: object):
        if not isinstance(other, QuiltUri):
            return NotImplemented
        return self.registry == other.registry and self.package == other.package

    def full_package(self) -> str | bool:
        return self.attrs.get(QuiltUri.K_PKG) or False

    def split_package(self, key) -> str | bool:
        sep = QuiltUri.SEP[key]
        pkg = self.full_package()
        if isinstance(pkg, str) and sep in pkg:
            s = pkg.split(sep)
            self.attrs[key] = s[1]
            return s[0]
        return False

    def parse_package(self) -> str | bool:
        return (
            self.split_package(QuiltUri.K_HASH)
            or self.split_package(QuiltUri.K_TAG)
            or self.full_package()
        )

    def has_package(self) -> bool:
        return QuiltUri.SEP[QuiltUri.K_PKG] in self.package if self.package else False
