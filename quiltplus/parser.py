import importlib.resources
from urllib.parse import parse_qs, urlparse

import quiltplus

from .package import QuiltPackage
from .schema import load_schemas

K_PKG = "package"
K_HASH = "top_hash"
K_TAG = "tag"


def parse_fragments(fragment):
    list_dict = parse_qs(fragment)
    scalars = {k: v[0] for k, v in list_dict.items()}
    return scalars


def parse_package(components):
    if K_PKG not in components:
        return False
    pkg = components[K_PKG]
    if "@" in pkg:
        s = pkg.split("@")
        components[K_HASH] = s[1]
        components[K_PKG] = s[0]
    if ":" in pkg:
        s = pkg.split(":")
        components[K_TAG] = s[1]
        components[K_PKG] = s[0]
    return True


class QuiltParser:

    CONF_DIR = importlib.resources.files(quiltplus)
    CONF_FILE = CONF_DIR / "config" / "schemas.yml"

    def __init__(self, config=CONF_FILE):
        self.schemas = load_schemas(config)

    def parse_uri(self, uri_string):
        uri = urlparse(uri_string)
        components = parse_fragments(uri.fragment)
        reg = "s3://" + uri.netloc
        parse_package(components)
        return self.schemas["URI"](registry=reg, **components)

    def parse_package(self, uri_string):
        uri = self.parse_uri(uri_string)
        if uri.package:
            return QuiltPackage(uri)
        return None
        # registry
        # path
        # property
