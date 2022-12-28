import importlib.resources

import pytest
import yaml

import tests
from quiltplus.schema import schema2class

TDIR = importlib.resources.files(tests)
TEST_FILE = TDIR / "examples" / "schemas.yml"
TEST_YAML = TEST_FILE.read_text()
TEST_DICT = yaml.safe_load(TEST_YAML)
URI_KEY = "QuiltPlusURI"


def test_imports():
    assert "test" in str(TDIR)
    assert "yml" in str(TEST_FILE)
    assert "Quilt" in TEST_YAML
    assert URI_KEY in TEST_DICT


def test_make_dataclass():
    KEY = "Ktest"
    dict = {"field": "str"}
    klass = schema2class(KEY, dict)
    assert klass
    inst = klass("string")
    assert inst
    assert isinstance(inst, klass)


def untest_schema2class():
    fields = TEST_DICT[URI_KEY]
    assert fields
    klass = schema2class(URI_KEY, fields)
    uri_class = globals()[URI_KEY]
    assert uri_class
    assert klass == uri_class
