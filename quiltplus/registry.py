from quilt3 import list_packages  # type: ignore

from .root import QuiltRoot


class QuiltRegistry(QuiltRoot):
    """Creates registry object from QuiltID."""

    def __init__(self, attrs: dict):
        super().__init__(attrs)
        self.attrs = attrs

    def __repr__(self):
        return f"QuiltRegistry({self.registry})"

    def url(self, pkg: str):
        """Convert package name to URL."""
        return self.pkg_uri(pkg) + ":latest"

    async def list(self, opts: dict = {}):
        """List package URIs in registry."""
        return [self.url(pkg) for pkg in list_packages(self.registry)]
