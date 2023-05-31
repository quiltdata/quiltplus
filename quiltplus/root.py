from .uri import QuiltUri


class QuiltRoot(QuiltUri):
    def __init__(self, attrs: dict):
        super().__init__(attrs)

    def __repr__(self):
        return f"{__class__}({self.attrs})"

    def base_uri(self):
        return f"quilt+{self.registry}"

    def pkg_uri(self, pkg=None):
        return self.base_uri() + f"#package={pkg or self.full_package()}"
