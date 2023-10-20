from quiltcore import Resource
from un_yaml import UnUri  # type: ignore


class QuiltType:
    PREFIX = "quilt+"
    K_BKT = UnUri.K_HOST
    K_DIR = "dir"
    K_FILE = "file"
    K_FORCE = "force"
    K_FAIL = "fallible"
    K_REG = "registry"

    # Fragments
    K_PKG = "package"
    K_PTH = "path"
    K_PRP = "property"
    K_CAT = "catalog"
    FRAG_KEYS = [K_PRP, K_PTH, K_PKG]

    # Decomposed Package Name
    SEP_HASH = "@"
    SEP_TAG = ":"
    SEP_PKG = "/"
    K_HASH = "_hash"
    K_TAG = "_tag"
    K_VER = "_version"
    SEP = {K_HASH: SEP_HASH, K_TAG: SEP_TAG, K_PKG: SEP_PKG}
    K_PKG_NAME = "_package_name"
    K_PKG_PRE = "_package_prefix"
    K_PKG_SUF = "_package_suffix"

    @staticmethod
    def BaseType(attrs: dict) -> str:
        for key in QuiltType.FRAG_KEYS:
            if key in attrs:
                return key
        return UnUri.K_HOST

    @staticmethod
    def Type(attrs: dict) -> str:
        type = QuiltType.BaseType(attrs)
        if type != QuiltType.K_PKG:
            return type
        pkg = attrs.get(QuiltType.K_PKG)
        if pkg and (QuiltType.SEP_HASH in pkg or QuiltType.SEP_TAG in pkg):
            return QuiltType.K_PKG
        return QuiltType.K_VER

    @staticmethod
    def Now() -> str:
        return Resource.Now()
