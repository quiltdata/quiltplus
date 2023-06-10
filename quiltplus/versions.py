from quilt3 import list_package_versions  # type: ignore

from .package import QuiltPackage


class QuiltVersions(QuiltPackage):
    """Creates versions manager for a package."""

    def __init__(self, attrs: dict):
        super().__init__(attrs)

    def url(self, hash: str):
        """Pin package name to specific version."""
        return self.pkg_uri() + f"@{hash}"

    async def list(self, opts: dict = {}):
        """List version URIs in package."""
        return [
            self.url(hash)
            for _pkg, hash in list_package_versions(self.package, self.registry)
        ]
