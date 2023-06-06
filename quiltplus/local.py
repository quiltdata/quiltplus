import logging
import os
import platform
import subprocess
from collections.abc import Generator
from filecmp import dircmp
from pathlib import Path
from tempfile import TemporaryDirectory

from quilt3.backends import get_package_registry  # type: ignore

from .root import QuiltRoot


class QuiltLocal(QuiltRoot):
    @staticmethod
    def TempDir() -> Generator[Path, None, None]:
        test_dir = os.environ.get("GITHUB_WORKSPACE")
        with TemporaryDirectory(ignore_cleanup_errors=True) as tmpdirname:
            tmpdir = Path(tmpdirname)
            if not test_dir:
                # logging.info(f"Creating {tmpdirname} on {platform.system()}")
                yield tmpdir
            else:
                temp_dir = Path(test_dir) / tmpdir.name
                # logging.info(f"Creating {temp_dir} on {platform.system()}")
                temp_dir.mkdir(parents=True, exist_ok=True)
                yield temp_dir
            logging.debug(f"Removing {tmpdirname} on {platform.system()}")

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
        super().__init__(attrs)
        self.local_registry = get_package_registry()
        for tmp in QuiltLocal.TempDir():
            logging.info(f"Package using QuiltLocal.TempDir: {tmp}")
            self.last_path = tmp

    def check_dir(self, path: Path | None = None):
        if not path:
            return self.last_path

        self.last_path = path
        if not path.exists():
            logging.warning(f"Path does not exist: {path}")
            path.mkdir(parents=True, exist_ok=True)
        elif not path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")
        return path

    def check_path(self, opts: dict):
        path = opts.get(QuiltLocal.K_PTH)
        return self.check_dir(path)

    def local_path(self, *paths: str):
        p = self.check_dir()
        for path in paths:
            p = p / path

        p.mkdir(parents=True, exist_ok=True)
        return p

    def local_files(self):
        root = self.local_path()
        return [
            os.path.relpath(os.path.join(dir, file), root)
            for (dir, dirs, files) in os.walk(root)
            for file in files
        ]

    def dest(self):
        return str(self.local_path())  # + "/"

    def local_cache(self) -> Path:
        base_path = Path(self.local_registry.base.path)
        if not base_path.exists():
            logging.warning(f"local_cache does not exist: {base_path}")
        return base_path / self.package

    def _diff(self) -> dict[str, str]:
        """Compare files in local_path to local cache"""
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
