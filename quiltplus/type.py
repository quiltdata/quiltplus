from datetime import datetime
from tzlocal import get_localzone

from udc import K_HOST


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
    K_HASH = "_hash"
    K_TAG = "_tag"
    K_VER = "_version"
    SEP = {
        K_HASH: SEP_HASH,
        K_TAG: SEP_TAG,
    }

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
        tz = get_localzone()
        dt = datetime.now(tz)
        dts = dt.replace(microsecond=0)
        return dts.isoformat()
