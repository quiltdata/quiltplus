import logging
from pathlib import Path
from tempfile import TemporaryDirectory

from quilt3.backends import get_package_registry  # type: ignore
from quiltcore.volume import Volume

from .root import QuiltRoot


class QuiltLocal(QuiltRoot):
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
        self.assign_dir()

    def assign_dir(self, local_dir: Path | None = None):
        if not local_dir:
            self.temp_dir = TemporaryDirectory(ignore_cleanup_errors=True)
            local_dir = Path(self.temp_dir.name)
        self.last_path = local_dir
        self.volume = Volume(self.last_path)
        return self.last_path

    def __del__(self):
        if hasattr(self, "temp_dir") and self.temp_dir:
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
        >>> loc.check_dir(Path(".")) == Path(".").resolve()
        True
        >>> new_dir = loc.check_dir(Path("test_nonexistent/"))
        >>> not_windows = not sys.platform.startswith("win")
        >>> new_dir.exists() if not_windows else True
        True
        >>> format_dir = loc.check_dir(Path("{package}")).as_posix()
        >>> str(format_dir).endswith("test_pkg/data")
        True
        >>> shutil.rmtree(new_dir)
        >>> shutil.rmtree(format_dir)
        """
        if not local_dir:
            return self.last_path

        dir_str = str(local_dir)
        logging.debug(f"check_dir: {local_dir} => {dir_str}")
        dir_var = dir_str.format(**self.attrs)
        logging.debug(f"check_dir: {dir_var} <= {self.attrs}")
        local_dir = Path(dir_var).resolve()

        if not local_dir.exists():
            logging.warning(f"Path does not exist: {local_dir}")
            local_dir.mkdir(parents=True, exist_ok=True)
        elif not local_dir.is_dir():
            raise ValueError(f"Path is not a directory: {local_dir}")

        return self.assign_dir(local_dir)

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

    def write_text(self, text: str, file: str, *paths: str):
        dir = self.local_path(*paths)
        p = dir / file
        p.write_text(text)
        return p
