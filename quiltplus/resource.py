from .uri import QuiltUri
from .property import QuiltProperty
from .path import QuiltPath
from .package import QuiltPackage
from .registry import QuiltRegistry
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

