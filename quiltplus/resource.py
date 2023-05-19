from .id import QuiltID
from .package import QuiltPackage
from .parse import K_BKT, K_PKG, K_PTH, K_VER
from .registry import QuiltRegistry
from .versions import QuiltVersions


def QuiltResource(uri: str):
    id = QuiltID(uri)
    t = id.type()
    if t == K_PTH:
        return QuiltPackage(id)
    elif t == K_VER:
        return QuiltVersions(id)
    elif t == K_PKG:
        return QuiltPackage(id)
    elif t == K_BKT:
        return QuiltRegistry(id)
    else:
        raise ValueError(f"Unknown resource type: {t}")
