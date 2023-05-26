from .parse import K_HOST, K_PKG, K_PROT, K_URI


class QuiltRoot:
    def __init__(self, attrs: dict):
        self.attrs = attrs
        self.root_uri = attrs[K_URI]

    def __repr__(self):
        return f"QuiltRoot({self.attrs})"

    def pkg(self):
        return self.attrs.get(K_PKG)

    def registry(self):
        return f"{self.attrs[K_PROT]}://{self.attrs[K_HOST]}"

    def base_uri(self):
        return f"quilt+{self.registry()}"

    def pkg_uri(self, pkg=None):
        return f"quilt+{self.registry()}#package={pkg or self.pkg()}"
