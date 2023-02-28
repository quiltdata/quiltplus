import yaml

from quiltplus.cache import *
from quiltplus.cli import *
from quiltplus.config import *
from quiltplus.id import *
from quiltplus.package import *
from quiltplus.parse import *
from quiltplus.unparse import *


def default_representer(dumper, data):
    # Alternatively, use repr() instead str():
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data))


yaml.representer.SafeRepresenter.add_representer(None, default_representer)
