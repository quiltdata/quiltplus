import importlib.resources

import fondat
import pytest
import yaml

import tests

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


def test_schema2class():
    schema = TEST_DICT[URI_KEY]
    assert schema
