# Create Quilt URI from UnURI attributes

from un_yaml import UnUri  # type: ignore

from .type import QuiltType


class QuiltUri(QuiltType):
    """
    Create and manage Quilt Resources from UnURI attrs.
    """

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
        """
        Set local variables and additional attributes.
        
        >>> reg = "s3://quilt-example"
        >>> pkg = "quilt/data"
        >>> pkg_full = f"{pkg}:latest"
        >>> path = "foo/bar"
        >>> uri = f"{QuiltUri.PREFIX}{reg}#package={pkg_full}&path={path}"
        >>> attrs = UnUri(uri).attrs
        >>> quilt = QuiltUri(attrs)
        >>> quilt.uri == uri
        True
        >>> quilt.registry == reg
        True
        >>> quilt.package == pkg
        True
        >>> quilt.attrs[QuiltUri.K_PKG] == pkg_full
        True
        >>> quilt.attrs[QuiltUri.K_PKG_NAME]
        'quilt/data'
        >>> quilt.attrs[QuiltUri.K_PKG_PRE]
        'quilt'
        >>> quilt.attrs[QuiltUri.K_PKG_SUF]
        'data'
        >>> quilt.attrs[QuiltUri.K_PTH] == path
        True
        """
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

    def parse_package(self) -> str:
        package = (
            self.split_package(QuiltUri.K_HASH)
            or self.split_package(QuiltUri.K_TAG)
            or self.full_package()
        )
        sep = QuiltUri.SEP[QuiltUri.K_PKG]
        if not isinstance(package, str) or sep not in package:
            return ""

        split = package.split(sep)
        self.attrs[QuiltUri.K_PKG_NAME] = package
        self.attrs[QuiltUri.K_PKG_PRE] = split[0]
        self.attrs[QuiltUri.K_PKG_SUF] = split[1]
        return package

    def has_package(self) -> bool:
        return QuiltUri.SEP[QuiltUri.K_PKG] in self.package if self.package else False
