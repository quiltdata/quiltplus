from typing import Protocol, runtime_checkable


@runtime_checkable
class Listable(Protocol):
    async def list(self):
        """List contents of URI."""
        return []


@runtime_checkable
class Getable(Protocol):
    async def get(self, path: str):
        """Get contents of URI into path"""
        return None


@runtime_checkable
class Putable(Protocol):
    async def put(self, path: str):
        """Put contents of path into URI."""
        return None
