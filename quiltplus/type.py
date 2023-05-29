from udc import K_HOST, UnUri
from datetime import datetime

class QuiltType:
    PREFIX = "quilt+"
    K_BKT = K_HOST

    # Fragments
    K_PKG = "package"
    K_PTH = "path"
    K_PRP = "property"
    K_CAT = "catalog"
    FRAG_KEYS = [K_PRP, K_PTH, K_PKG]

    # Decomposed Package Name
    SEP_HASH = "@"
    SEP_TAG = ":"
    K_HSH = "_hash"
    K_TAG = "_tag"
    K_VER = "_version"

    @staticmethod
    def BaseType(attrs: dict) -> str:
        for key in QuiltType.FRAG_KEYS:
            if key in attrs:
                return key
        return K_HOST

    @staticmethod
    def Type(attrs: dict) -> str:
        type = QuiltType.BaseType(attrs)
        if type != QuiltType.K_PKG:
            return type
        pkg = attrs.get(QuiltType.K_PKG)
        if QuiltType.SEP_HASH in pkg or QuiltType.SEP_TAG in pkg:
            return QuiltType.K_PKG
        return QuiltType.K_VER

    @staticmethod
    def Now() -> str:
        return datetime.now().isoformat()