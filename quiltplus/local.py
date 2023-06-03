import logging
import os
import platform
import subprocess
from collections.abc import Generator
from pathlib import Path
from tempfile import TemporaryDirectory

from .root import QuiltRoot


class QuiltLocal(QuiltRoot):
    @staticmethod
    def TempDir() -> Generator[Path, None, None]:
        with TemporaryDirectory(ignore_cleanup_errors=True) as tmpdirname:
            tmpdir = Path(tmpdirname)
            yield (tmpdir)
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
        for tmp in QuiltLocal.TempDir():
            self.last_path = tmp

    def check_dir(self, path: Path | None = None):
        if not path:
            return self.last_path

        self.last_path = path
        if not path.exists():
            logging.warn(f"Path does not exist: {path}")
            path.mkdir(parents=True, exist_ok=True)
        elif not path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")
        return path

    def check_path(self, opts: dict):
        path = opts.get(QuiltLocal.K_PTH)
        print(path)
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

    def write_text(self, text: str, file: str, *paths: str):
        dir = self.local_path(*paths)
        p = dir / file
        p.write_text(text)
        return p

    def open(self):
        return QuiltLocal.OpenDesktop(self.dest())
