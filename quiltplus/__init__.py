import yaml
from quiltplus.cache import QuiltIdCache  # NOQA F401
from quiltplus.cli import cli  # NOQA F401
from quiltplus.config import QuiltConfig  # NOQA F401
from quiltplus.id import QuiltID  # NOQA F401
from quiltplus.ignore import GitIgnore  # NOQA F401
from quiltplus.package import QuiltPackage  # NOQA F401
from quiltplus.parse import K_BKT, K_HSH, K_PKG, K_PTH, K_STR, QuiltParse  # NOQA F401
from quiltplus.unparse import QuiltUnparse  # NOQA F401


def default_representer(dumper, data):
    # Alternatively, use repr() instead str():
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data))


yaml.representer.SafeRepresenter.add_representer(None, default_representer)
