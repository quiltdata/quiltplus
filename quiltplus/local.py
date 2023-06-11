import logging
import os
import platform
import subprocess
from filecmp import dircmp
from pathlib import Path
from tempfile import TemporaryDirectory

from quilt3.backends import get_package_registry  # type: ignore

from .root import QuiltRoot


class QuiltLocal(QuiltRoot):
    @staticmethod
    def OpenDesktop(dest: str):
        if platform.system() == "Windows":
            os.startfile(dest)  # type: ignore
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-R", dest])
        else:
            subprocess.Popen(["xdg-open", dest])
        return dest

    def __init__(self, attrs: dict):
        """
        Base class to set and manage local sync directory
        (starting with a temporary one).

        >>> loc = QuiltLocal({"package": "test/data"})
        >>> loc.last_path.exists()
        True
        >>> loc.last_path.is_dir()
        True
        """
        super().__init__(attrs)
        self.local_registry = get_package_registry()
        logging.debug(f"get_package_registry(): {self.local_registry}")
        self.make_temp_dir()

    def make_temp_dir(self):
        self.temp_dir: TemporaryDirectory = TemporaryDirectory(
            ignore_cleanup_errors=True
        )
        self.last_path = Path(self.temp_dir.name)

    def __del__(self):
        self.temp_dir.cleanup()

    def check_dir(self, local_dir: Path | None = None):
        """
        Check if local_dir exists and is a directory.
        If local_dir is None, return the last path used.
        If it does not exist, create it.
        If an attrs variable, expand it

        Args:
            local_dir (Path): Path to check (optional)

        Returns:
            Path: Path to local_dir (gauranteed to exist)

        Raises:
            ValueError: If local_dir is not a directory

        >>> import shutil, sys
        >>> loc = QuiltLocal({"package": "test_pkg/data"})
        >>> loc.check_dir() == loc.last_path
        True
        >>> local_file = loc.last_path / "TEST.txt"
        >>> local_file.touch()
        >>> loc.check_dir(local_file)  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        ValueError: Path is not a directory...
        >>> loc.check_dir(Path(".")) == Path(".")
        True
        >>> new_dir = loc.check_dir(Path("test_nonexistent/"))
        >>> new_dir.exists() if not sys.platform.startswith("win") else True
        True
        >>> format_dir = loc.check_dir(Path("{package}"))
        >>> str(format_dir) if not sys.platform.startswith("win") else str(format_dir).replace("\\", "/")
        'test_pkg/data'
        >>> shutil.rmtree(new_dir)
        >>> shutil.rmtree(format_dir)
        """
        if not local_dir:
            return self.last_path

        if str(local_dir).startswith("{"):
            local_dir = Path(str(local_dir).format(**self.attrs))

        self.last_path = local_dir
        if not local_dir.exists():
            logging.warning(f"Path does not exist: {local_dir}")
            local_dir.mkdir(parents=True, exist_ok=True)
        elif not local_dir.is_dir():
            raise ValueError(f"Path is not a directory: {local_dir}")
        return local_dir

    def check_dir_arg(self, opts: dict):
        local_dir = opts.get(QuiltLocal.K_DIR)
        return self.check_dir(local_dir)

    def local_path(self, *paths: str) -> Path:
        p = self.check_dir()
        for path in paths:
            p = p / path

        p.mkdir(parents=True, exist_ok=True)
        return p

    def local_files(self) -> list[Path]:
        root = self.local_path()
        return [f for f in root.rglob("*") if f.is_file()]

    def dest(self):
        return str(self.local_path())

    def local_cache(self) -> Path:
        base_path = Path(self.local_registry.base.path)
        logging.debug(f"local_registry.base.path: {base_path}")
        if not base_path.exists():
            logging.warning(f"local_cache does not exist: {base_path}")
        return base_path / self.package

    def _diff(self) -> dict[str, str]:
        """Compare files in local_dir to local cache"""
        cache = self.local_cache()
        if not cache.exists():
            logging.warning(f"_diff: local_cache[{cache}] does not exist")
            return {}
        diff = dircmp(str(cache), self.dest())
        # logging.debug(f"_diff.diff: {diff}")
        results = {
            "add": diff.right_only,
            "rm": diff.left_only,
            "touch": diff.diff_files,
        }
        return {
            filename: stage
            for stage, sublist in results.items()
            for filename in sublist
        }

    def write_text(self, text: str, file: str, *paths: str):
        dir = self.local_path(*paths)
        p = dir / file
        p.write_text(text)
        return p

    def open(self):
        return QuiltLocal.OpenDesktop(self.dest())
