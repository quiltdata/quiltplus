import yaml

from .cache import QuiltIdCache  # NOQA F401
from .cli import cli  # NOQA F401
from .config import QuiltConfig  # NOQA F401
from .id import QuiltID  # NOQA F401
from .ignore import GitIgnore  # NOQA F401
from .package import QuiltPackage  # NOQA F401
from .parse import (K_BKT, K_HSH, K_PKG, K_PRP, K_PTH,  # NOQA F401
                             K_STR, K_VER, QuiltParse)
from .resource import QuiltResource  # NOQA F401
from .registry import QuiltRegistry  # NOQA F401
from .unparse import QuiltUnparse  # NOQA F401
from .versions import QuiltVersions  # NOQA F401


def default_representer(dumper, data):
    # Alternatively, use repr() instead of str():
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data))


yaml.representer.SafeRepresenter.add_representer(None, default_representer)
