import logging
import os
import re
from datetime import datetime
from pathlib import Path

import yaml

from .id import QuiltID


class QuiltConfig:
    CATALOG_FILE = "CATALOG.webloc"
    CONFIG_FOLDER = ".quilt"
    CONFIG_YAML = "config.yaml"
    K_QC = "quiltconfig"
    K_URI = "uri"
    REVISEME_FILE = "REVISEME.webloc"

    @staticmethod
    def AsConfig(uri):
        obj = {QuiltConfig.K_QC: {QuiltConfig.K_URI: uri}}
        return yaml.safe_dump(obj)

    @staticmethod
    def AsShortcut(uri):
        return f"[InternetShortcut]\nURL={uri}"

    @staticmethod
    def AsWebloc(uri):
        return f'{{ URL = "{uri}"; }}'

    @staticmethod
    def ForRoot(root: Path):
        return QuiltConfig(str(root / QuiltConfig.CONFIG_FOLDER))

    @staticmethod
    def Now():
        return datetime.now().astimezone().replace(microsecond=0).isoformat()

    def __init__(self, config_location: str):
        # determine if folder or file, then set both
        loc = Path(config_location)
        is_file = loc.is_file() if loc.exists() else re.match(r"y?ml", loc.suffix)
        self.file = loc if is_file else loc / QuiltConfig.CONFIG_YAML
        self.path = loc.parents[0] if is_file else loc
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
        self.write_config(QuiltConfig.CONFIG_YAML, QuiltConfig.AsConfig(pkg_uri))
        return [
            QuiltConfig.CATALOG_FILE,
            QuiltConfig.REVISEME_FILE,
            QuiltConfig.CONFIG_YAML,
        ]

    def get_uri(self):
        if not self.file.exists():
            logging.info(f"NOT_FOUND QuiltConfig.get_uri({self.file})")
            return None
        cfg_yaml = self.file.read_text()
        logging.debug(f"QuiltConfig.GetURI.cfg_yaml: {cfg_yaml}")
        cfg = yaml.safe_load(cfg_yaml)
        logging.debug(f"QuiltConfig.GetURI.cfg: {cfg}")
        config = cfg.get(QuiltConfig.K_QC)
        if not config:
            logging.info(f"NOT_FOUND '{QuiltConfig.K_QC}' in {self.file}")
            return None
        return config.get(QuiltConfig.K_URI)
