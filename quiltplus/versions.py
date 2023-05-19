from quilt3 import list_package_versions
from typing_extensions import Self

from .id import QuiltID


class QuiltVersions:
    """Creates versions manager for a package."""

    def __init__(self, id: QuiltID):
        self.id = id
        self.registry = id.registry()
        self.pkg = id.pkg()

    def __repr__(self):
        return f"QuiltVersions({self.registry})"

    def __eq__(self, other: Self):
        return self.registry == other.registry

    def url(self, hash: str):
        """Convert package name to URL."""
        return self.id.quilt_uri() + f"@{hash}"

    async def list(self):
        """List version URIs in package."""
        return [
            self.url(hash)
            for pkg, hash in list_package_versions(self.pkg, self.registry)
        ]
