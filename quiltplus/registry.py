from quilt3 import list_packages
from typing_extensions import Self

from .root import QuiltRoot


class QuiltRegistry(QuiltRoot):
    """Creates registry object from QuiltID."""

    def __init__(self, attrs: dict):
        super().__init__(attrs)
        self.attrs = attrs

    def __repr__(self):
        return f"QuiltRegistry({self.registry()})"

    def __eq__(self, other: Self):
        return self.registry() == other.registry()

    def url(self, pkg: str):
        """Convert package name to URL."""
        return self.pkg_uri(pkg) + ":latest"

    async def list(self):
        """List package URIs in registry."""
        return [self.url(pkg) for pkg in list_packages(self.registry())]
