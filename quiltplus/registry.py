from quilt3 import list_packages  # type: ignore
from quiltcore import Resource, Registry

from .root import QuiltRoot


class QuiltRegistry(QuiltRoot):
    """Creates registry object from QuiltID."""

    @classmethod
    def PackageName(cls, name: Resource):
        """Convert package name to registry name."""
        return "/".join(name.path.parts[-2:])

    def __init__(self, attrs: dict):
        super().__init__(attrs)
        self.attrs = attrs
        self.core = Registry.FromURI(self.registry)

    def url(self, pkg: str):
        """Convert package name to URL."""
        return self.pkg_uri(pkg) + ":latest"


    async def list(self, opts: dict = {}):
        """List package URIs in registry."""
        pkg_names = [self.PackageName(name) for name in self.core.list()]
        return [self.url(pkg) for pkg in pkg_names]
