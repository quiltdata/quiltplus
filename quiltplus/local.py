import os
import logging
import platform
import subprocess
from pathlib import Path

from .root import QuiltRoot


class QuiltLocal(QuiltRoot):

    @staticmethod
    def OpenDesktop(dest: str):
        if platform.system() == "Windows":
            os.startfile(dest)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-R", dest])
        else:
            subprocess.Popen(["xdg-open", dest])
        return dest

    def __init__(self, attrs: dict):
        super().__init__(attrs)
        self.check_dir(Path.cwd())

    def check_dir(self, path: Path):
        if not path:
            return self.last_path
        self.last_path = path
        if not path.exists():
            logging.warn(f"Path does not exist: {path}")
            path.mkdir(parents=True, exist_ok=True)
        elif not path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")
        return path

    def local_path(self, *paths: str):
        p = self.last_path
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

