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
        >>> loc.dir_path.exists()
        True
        >>> loc.dir_path.is_dir()
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
        self.dir_path = Path(self.temp_dir.name)

    def __del__(self):
        self.temp_dir.cleanup()

    def check_dir_arg(self, opts: dict):
        local_dir = opts.get(QuiltLocal.K_DIR)
        return self.check_dir(local_dir)

    def local_path(self, *paths: str) -> Path:
        return self.dir(*paths)

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

    def open(self):
        return QuiltLocal.OpenDesktop(self.dest())
