import importlib.resources
from typing import Any, Generic, Literal, Optional, TypedDict, TypeVar, Union

import pytest
import yaml

import tests
from quiltplus.schema import *

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


def test_parse_field():
    assert parse_field("a", "str") == ("a", str)
    assert parse_field("a", "str='hello'")[2].default == "hello"

    result = parse_field("?a", "str")
    assert result[0] == "a"
    assert result[2].default == None
    assert result[1] == Optional[str]

    result = parse_field("?a", "str='hello'")
    assert result[0] == "a"
    assert result[2].default == "hello"
    assert result[1] == Optional[str]


def test_make_dataclass():
    KEY = "Ktest"
    dict = {"init": "bool", "?field": "str='hi'"}
    klass = schema2class(KEY, dict)
    assert klass
    inst = klass(True)
    assert inst
    assert isinstance(inst, klass)
    assert inst.field == "hi"

    inst2 = klass(False, "bye")
    assert inst2.field == "bye"


def test_schema2class():
    fields = TEST_DICT[URI_KEY]
    print(fields)
    assert fields
    klass = schema2class(URI_KEY, fields)
    inst = klass("s3://quilt-examples")
    assert inst
    assert isinstance(inst, klass)


def test_load_schemas():
    klasses = load_schemas(TEST_FILE)
    inst = klasses[2](["."])
    assert inst
