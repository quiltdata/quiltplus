from quilt3 import list_packages
from typing_extensions import Self

from .id import QuiltID


class QuiltRegistry:
    """Creates registry object from QuiltID."""

    def __init__(self, id: QuiltID):
        self.id = id
        self.registry = id.registry()

    def __repr__(self):
        return f"QuiltRegistry({self.registry})"

    def __eq__(self, other: Self):
        return self.registry == other.registry

    def url(self, pkg: str):
        """Convert package name to URL."""
        return self.id.quilt_uri() + f"#package={pkg}:latest"

    async def list(self):
        """List package URIs in registry."""
        return [self.url(pkg) for pkg in list_packages(self.registry)]
