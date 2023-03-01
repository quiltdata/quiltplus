import yaml
from quiltplus.cache import QuiltIdCache
from quiltplus.cli import cli
from quiltplus.config import QuiltConfig
from quiltplus.id import QuiltID
from quiltplus.ignore import GitIgnore
from quiltplus.package import QuiltPackage
from quiltplus.parse import K_BKT, K_HSH, K_PKG, K_PTH, K_STR, QuiltParse
from quiltplus.unparse import QuiltUnparse


def default_representer(dumper, data):
    # Alternatively, use repr() instead str():
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data))


yaml.representer.SafeRepresenter.add_representer(None, default_representer)
