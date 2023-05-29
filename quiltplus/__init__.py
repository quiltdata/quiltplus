import yaml

from .ignore import GitIgnore  # NOQA F401
from .package import QuiltPackage  # NOQA F401
from .registry import QuiltRegistry  # NOQA F401
from .resource import QuiltResource  # NOQA F401
from .type import QuiltType  # NOQA F401
from .uri import QuiltUri  # NOQA F401
from .versions import QuiltVersions  # NOQA F401


def default_representer(dumper, data):
    # Alternatively, use repr() instead of str():
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data))


yaml.representer.SafeRepresenter.add_representer(None, default_representer)
