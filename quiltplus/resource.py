from .package import QuiltPackage
from .path import QuiltPath
from .property import QuiltProperty
from .registry import QuiltRegistry
from .uri import QuiltUri
from .versions import QuiltVersions

KLASS_MAP = {
    QuiltUri.K_PKG: QuiltPackage,
    QuiltUri.K_PRP: QuiltProperty,
    QuiltUri.K_PTH: QuiltPath,
    QuiltUri.K_BKT: QuiltRegistry,
    QuiltUri.K_VER: QuiltVersions,
}


def QuiltResource(attrs: dict):
    type = QuiltUri.Type(attrs)
    klass = KLASS_MAP[type]
    return klass(attrs)


def QuiltResourceURI(uri: str):
    attrs = QuiltUri.AttrsFromUri(uri)
    return QuiltResource(attrs)
