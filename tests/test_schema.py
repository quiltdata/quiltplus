from typing import Optional

import yaml

from quiltplus.parser import QuiltParser
from quiltplus.schema import *


def test_parse_field():
    assert parse_field("a", "str") == ("a", str)
    assert parse_field("a", "str='hello'")[2].default == "hello"
    assert parse_field("?a", "str") == ("a", Optional[str])

    result = parse_field("?a", "str='hello'")
    assert result[0] == "a"
    assert result[2].default == "hello"
    assert result[1] == Optional[str]


def test_make_dataclass():
    KEY = "K.test"
    dict = {"init": "bool", "?field": "str='hi'"}
    klass = schema2class(KEY, dict)
    assert klass
    inst = klass(init=True)
    assert inst
    assert isinstance(inst, klass)
    assert inst.field == "hi"

    inst2 = klass(init=False, field="bye")
    assert inst2.field == "bye"


def test_schema2class():
    TEST_YAML = QuiltParser.CONF_FILE.read_text()
    TEST_DICT = yaml.safe_load(TEST_YAML)
    URI_KEY = "URI"
    assert URI_KEY in TEST_DICT

    fields = TEST_DICT[URI_KEY]
    assert fields
    klass = schema2class(URI_KEY, fields)
    inst = klass(registry="s3://quilt-examples")
    assert inst
    assert isinstance(inst, klass)


def test_load_schemas():
    klasses = load_schemas(QuiltParser.CONF_FILE)
    inst = klasses["Path"](paths=["."])
    assert inst
