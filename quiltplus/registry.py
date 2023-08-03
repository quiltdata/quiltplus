from quiltcore import Resource

from .root import QuiltRoot


class QuiltRegistry(QuiltRoot):
    """Creates registry object from QuiltID."""

    @classmethod
    def PackageName(cls, name: Resource):
        """Convert package name to registry name."""
        return cls.SEP_PKG.join(name.path.parts[-2:])

    def __init__(self, attrs: dict):
        super().__init__(attrs)
        self.attrs = attrs

    def url(self, pkg: str):
        """Convert package name to URL."""
        return self.pkg_uri(pkg) + ":latest"

    async def list(self, opts: dict = {}):
        """List package URIs in registry."""
        pkg_names = [namespace.name for namespace in self.domain.list()]
        return [self.url(pkg) for pkg in pkg_names]
