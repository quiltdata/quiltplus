import logging
import os
from datetime import datetime
from pathlib import Path

import yaml

from .id import QuiltID


class QuiltConfig:
    CONFIG_FOLDER = ".quilt"
    REVISEME_FILE = "REVISEME.webloc"
    CATALOG_FILE = "CATALOG.webloc"
    CONFIG_YAML = "config.yaml"

    @staticmethod
    def Now():
        return datetime.now().astimezone().replace(microsecond=0).isoformat()

    @staticmethod
    def AsWebloc(uri):
        return f'{{ URL = "{uri}"; }}'

    @staticmethod
    def AsShortcut(uri):
        return f"[InternetShortcut]\nURL={uri}"

    @staticmethod
    def AsPackages(*uris):
        obj = {"packages": uris}
        return yaml.safe_dump(obj)

    def __init__(self, root: Path):
        self.path = root / QuiltConfig.CONFIG_FOLDER
        self.path.mkdir(parents=True, exist_ok=True)

    def __repr__(self):
        return f"QuiltConfig[{self.path})"

    def __str__(self):
        return self.__repr__()

    def list_config(self):
        return [
            os.path.relpath(os.path.join(dir, file), self.path)
            for (dir, dirs, files) in os.walk(self.path)
            for file in files
        ]

    def write_config(self, file: str, text: str):
        p = self.path / file
        p.write_text(text)
        return p

    def save_webloc(self, file: str, uri: str):
        shortcut_file = file.replace("webloc", "URL")
        path = self.write_config(shortcut_file, QuiltConfig.AsShortcut(uri))
        path = self.write_config(file, QuiltConfig.AsWebloc(uri))
        return path

    def save_config(self, id: QuiltID):
        pkg_uri = id.quilt_uri()
        cat_uri = id.catalog_uri()
        self.save_webloc(QuiltConfig.CATALOG_FILE, cat_uri)
        self.save_webloc(QuiltConfig.REVISEME_FILE, f"{cat_uri}?action=revisePackage")
        self.write_config(QuiltConfig.CONFIG_YAML, QuiltConfig.AsPackages(pkg_uri))
        return [
            QuiltConfig.CATALOG_FILE,
            QuiltConfig.REVISEME_FILE,
            QuiltConfig.CONFIG_YAML,
        ]
