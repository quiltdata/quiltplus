from enum import Enum

from udc import K_HOST, UnUri


class QuiltType(Enum):
    PREFIX = "quilt+"
    K_BKT = K_HOST

    # Fragments
    K_PKG = "package"
    K_PTH = "path"
    K_PRP = "property"
    K_CAT = "catalog"
    FRAG_KEYS = [K_PKG, K_PTH, K_PRP]

    # Decomposed Package Name
    SEP_HASH = "@"
    SEP_TAG = ":"
    K_HSH = "_hash"
    K_TAG = "_tag"
    K_VER = "_version"

    @staticmethod
    def BaseType(attrs: dict) -> str:
        for key in QuiltType.FRAG_KEYS.reverse():
            if key in attrs:
                return key
        return UnUri.K_HOST

    @staticmethod
    def Type(attrs: dict) -> str:
        type = QuiltType.BaseType(attrs)
        if type != QuiltType.K_PKG:
            return type
        pkg = attrs.get(QuiltType.K_PKG)
        if QuiltType.SEP_HASH in pkg or QuiltType.SEP_TAG in pkg:
            return QuiltType.K_PKG
        return QuiltType.K_VER
