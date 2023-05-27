from .id import QuiltID
from .package import QuiltPackage
from .parse import K_BKT, K_PKG, K_PRP, K_PTH, K_TOOL, K_VER
from .registry import QuiltRegistry
from .versions import QuiltVersions

TOOL = "quilt"


def QuiltType(attrs: dict):
        if TOOL != attrs[K_TOOL]:
            raise ValueError(f"Error: URI scheme does not start with {TOOL}: {attrs}")
        type = K_BKT
        if K_PRP in attrs:
            type = K_PRP
        elif K_PTH in attrs:
            type = K_PTH
        return type

def QuiltResourceURI(uri: str):
    id = QuiltID(uri)
    attrs = id.attrs
    t = id.type() # QuiltType(attrs)

    if t == K_PTH:
        return QuiltPackage(attrs)
    elif t == K_VER:
        return QuiltVersions(id)
    elif t == K_PKG:
        return QuiltPackage(attrs)
    elif t == K_BKT:
        return QuiltRegistry(attrs)
    else:
        raise ValueError(f"Unknown resource type: {t}")
