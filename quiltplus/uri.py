# Create Quilt URI from UnURI attributes

from udc import UnUri, K_HOST, K_PROT, K_URI

class QuiltUri:
    PREFIX = "quilt+"
    K_BKT = K_HOST

    ## Fragments

    K_PKG = "package"
    K_PTH = "path"
    K_PRP = "property"
    K_CAT = "catalog"

    FRAG_KEYS = [K_PKG, K_PTH, K_PRP]

    ## Decomponsed Package Name

    SEP_HASH = "@"
    SEP_TAG = ":"
    K_HSH = "_hash"
    K_TAG = "_tag"
    K_VER = "_version"

    @staticmethod
    def BaseType(attrs: dict):
        for key in QuiltUri.FRAG_KEYS:
            if key in attrs:
                return key
        return UnUri.K_HOST

    def __init__(self, attrs: dict):
        self.attrs = attrs
        self.uri = attrs.get(K_URI)
        self.registry = f"{attrs.get(K_PROT)}://{attrs.get(K_HOST)}"
        self.pkg = self.parse_package()
        self.type = self.parse_type()
      
    def __repr__(self):
        return f"QuiltUri({self.uri})"
    
    def get(self, key):
        return self.attrs.get(key)
    
    def split_package(self, key):
        pkg = self.get(QuiltUri.K_PKG)
        if not pkg or not key in pkg:
            return None
        s = pkg.split(key)
        self.attrs[key] = s[1]
        return s[0]

    def parse_package(self):
        return (self.split_package(QuiltUri.SEP_HASH) 
                or self.split_package(QuiltUri.SEP_TAG) 
                or self.get(QuiltUri.K_PKG)
        )

    def parse_type(self):
        type = QuiltUri.BaseType(self.attrs)
        if type == QuiltUri.K_PKG and self.pkg == self.get(QuiltUri.K_PKG):
            return QuiltUri.K_VER
        return type
        