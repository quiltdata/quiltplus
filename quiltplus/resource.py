from .id import QuiltID
from .package import QuiltPackage
from .registry import QuiltRegistry
from .versions import QuiltVersions
from .parse import K_BKT, K_PKG, K_PTH, K_VER

def QuiltResource(uri: str):
    id = QuiltID(uri)
    t = id.type()
    attrs = id.attrs
    if t == K_PTH:
        return QuiltPackage(attrs)
    elif t == K_VER:
        return QuiltVersions(id)
    elif t == K_PKG:
        return QuiltPackage(attrs)
    elif t == K_BKT:
        return QuiltRegistry(id)
    else:
        raise ValueError(f"Unknown resource type: {t}")
