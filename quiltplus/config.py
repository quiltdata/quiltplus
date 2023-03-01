import logging
import os
import re
from datetime import datetime
from importlib import metadata
from pathlib import Path

import yaml

from .id import QuiltID

__version__ = metadata.version(__package__)


class QuiltConfig:
    CATALOG_FILE = "CATALOG.webloc"
    CONFIG_FOLDER = ".quilt"
    CONFIG_YAML = "config.yaml"
    K_ACT = "action"
    K_DEP = "depend"
    K_NAM = "name"
    K_QC = "quiltconfig"
    K_REV = "revise"
    K_STG = "stage"
    K_URI = "uri"
    K_VER = "version"
    K_CAT = "view"
    REVISEME_FILE = "REVISEME.webloc"

    @staticmethod
    def AsShortcut(uri):
        return f"[InternetShortcut]\nURL={uri}"

    @staticmethod
    def AsWebloc(uri):
        return f'{{ URL = "{uri}"; }}'

    @staticmethod
    def BaseConfig():
        return {QuiltConfig.K_VER: __version__}

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
        return f"QuiltConfig['{self.path}')"

    def __str__(self):
        return self.__repr__()

    def list_config(self):
        return [
            os.path.relpath(os.path.join(dir, file), self.path)
            for (dir, dirs, files) in os.walk(self.path)
            for file in files
        ]

    def get_config(self):
        if not self.file.exists():
            return QuiltConfig.BaseConfig()

        cfg_yaml = self.file.read_text()
        logging.debug(f"QuiltConfig.GetURI.cfg_yaml: {cfg_yaml}")
        cfg = yaml.safe_load(cfg_yaml)
        logging.debug(f"QuiltConfig.GetURI.cfg: {cfg}")
        config = cfg.get(QuiltConfig.K_QC)
        if not config:
            logging.error(f"{self.file}: needs yaml key '{QuiltConfig.K_QC}'")
            return {}
        return config

    def write_file(self, file: str, text: str):
        p = self.path / file
        p.write_text(text)
        return p

    def update_config(self, options: dict, reset_stage: bool = False):
        config = self.get_config()
        for key in [QuiltConfig.K_URI, QuiltConfig.K_CAT, QuiltConfig.K_REV]:
            if key in options:
                config[key] = options[key]

        if QuiltConfig.K_DEP in options:
            depend = options[QuiltConfig.K_DEP]
            deps = self.get_depend()
            if depend[0] == "+":
                deps.add(depend[1:])
            else:
                deps.remove(depend[1:])
            config[QuiltConfig.K_DEP] = list(deps)

        if QuiltConfig.K_STG in options:
            stage = options[QuiltConfig.K_STG]
            stg = self.get_stage()
            name = stage[QuiltConfig.K_NAM]
            stg[name] = stage
            config[QuiltConfig.K_STG] = stg
        elif reset_stage:
            config[QuiltConfig.K_STG] = {}

        self.save_config(config)
        return config

    def save_config(self, config):
        root = {QuiltConfig.K_QC: config}
        yaml_str = yaml.safe_dump(root)
        self.file.write_text(yaml_str)

    def save_webloc(self, file: str, uri: str):
        shortcut_file = file.replace("webloc", "URL")
        path = self.write_file(shortcut_file, QuiltConfig.AsShortcut(uri))
        path = self.write_file(file, QuiltConfig.AsWebloc(uri))
        return path

    def save_uri(self, id: QuiltID):
        pkg_uri = id.quilt_uri()
        cat_uri = id.catalog_uri()
        rev_uri = f"{cat_uri}?action=revisePackage"
        self.save_webloc(QuiltConfig.CATALOG_FILE, cat_uri)
        self.save_webloc(QuiltConfig.REVISEME_FILE, rev_uri)
        options = {
            QuiltConfig.K_URI: pkg_uri,
            QuiltConfig.K_CAT: cat_uri,
            QuiltConfig.K_REV: rev_uri,
        }
        self.update_config(options)
        return [
            QuiltConfig.CATALOG_FILE,
            QuiltConfig.REVISEME_FILE,
            QuiltConfig.CONFIG_YAML,
        ]

    def get_uri(self, key=None):
        if not key:
            key = QuiltConfig.K_URI
        return self.get_config().get(key)

    def get_stage(self, adds=None):
        stg = self.get_config().get(QuiltConfig.K_STG, {})
        print(f"get_stage.stg: {stg}")
        if adds:
            return {k: v for (k, v) in stg.items() if v[QuiltConfig.K_ACT] == "add"}
        elif adds is False:
            return {k: v for (k, v) in stg.items() if v[QuiltConfig.K_ACT] != "add"}
        return stg

    def stage(self, file: str, is_add: bool = True):
        p = Path(file)
        if not p.exists():
            logging.error(f"MISSING_FILE: cannot stage file '{p}' that does not exist")
            return None
        stats = p.stat()
        attrs = {
            QuiltConfig.K_NAM: file,
            QuiltConfig.K_ACT: "add" if is_add else "remove",
            "size": stats.st_size,
            "created": stats.st_ctime,
            "updated": stats.st_mtime,
            "accessed": stats.st_atime,
        }
        self.update_config({QuiltConfig.K_STG: attrs})
        return attrs

    def get_depend(self):
        deps = self.get_config().get(QuiltConfig.K_DEP, [])
        return set(deps)

    def depend(self, uri: str, is_add: bool = True):
        key = f"+{uri}" if is_add else f"-{uri}"
        return self.update_config({QuiltConfig.K_DEP: key})
