from pathlib import Path
from tempfile import TemporaryDirectory

from .conftest import TEST_URL, QuiltConfig, QuiltID, logging, os, pytest

RM_LOCAL = os.path.join(QuiltConfig.CONFIG_FOLDER, QuiltConfig.REVISEME_FILE)


@pytest.fixture
def cfg():
    with TemporaryDirectory() as tmpdirname:
        config = QuiltConfig.ForRoot(Path(tmpdirname))
        logging.debug(config)
        yield config


def test_cfg_as():
    assert f"]\nURL={TEST_URL}" in QuiltConfig.AsShortcut(TEST_URL)
    assert f'{{ URL = "{TEST_URL}"; }}' in QuiltConfig.AsWebloc(TEST_URL)


def test_cfg_fixture(cfg: QuiltConfig):
    assert cfg


def test_cfg_write(cfg: QuiltConfig):
    p = cfg.write_file("test.txt", TEST_URL)
    assert QuiltConfig.CONFIG_FOLDER in str(p)
    assert "test.txt" in str(p)
    assert TEST_URL == p.read_text()


def test_cfg_update_uri(cfg: QuiltConfig):
    cf = cfg.update_config({QuiltConfig.K_URI: TEST_URL})
    assert TEST_URL == cf[QuiltConfig.K_URI]
    assert TEST_URL == cfg.get_uri()


def test_cfg_update_stage(cfg: QuiltConfig):
    staged = {"name": "filename"}
    cf = cfg.update_config({QuiltConfig.K_STG: staged})
    entry = cf[QuiltConfig.K_STG]
    assert entry is not None
    assert entry["filename"] == staged


def test_cfg_depend(cfg: QuiltConfig):
    uri = "s3//sample-uri"
    cf = cfg.depend(uri)
    assert uri in cf[QuiltConfig.K_DEP]

    cf = cfg.depend(uri, False)
    assert uri not in cf[QuiltConfig.K_DEP]


def test_cfg_save_webloc(cfg: QuiltConfig):
    p = cfg.save_webloc("test2.webloc", TEST_URL)
    assert QuiltConfig.CONFIG_FOLDER in str(p)
    assert "test2.webloc" in str(p)
    assert f'{{ URL = "{TEST_URL}"; }}' in p.read_text()

    files = cfg.list_config()
    assert "test2.webloc" in files
    assert "test2.URL" in files


def test_cfg_save_uri(cfg: QuiltConfig):
    qid = QuiltID(TEST_URL)
    configs = cfg.save_uri(qid)
    assert QuiltConfig.CONFIG_YAML in configs
    files = cfg.list_config()
    for cf in configs:
        assert cf in files

    p = cfg.path / QuiltConfig.CONFIG_YAML
    assert TEST_URL in p.read_text()
    assert TEST_URL == cfg.get_uri()
    assert QuiltID.DEFAULT_CATALOG in cfg.get_uri(QuiltConfig.K_CAT)


def test_cfg_get_config(cfg: QuiltConfig):
    config = cfg.get_config()
    assert config.get("version") is not None
    assert config.get(QuiltConfig.K_URI) is None
    qid = QuiltID(TEST_URL)
    cfg.save_uri(qid)
    config = cfg.get_config()
    assert config
    assert TEST_URL == config[QuiltConfig.K_URI]


def test_cfg_get_uri(cfg: QuiltConfig):
    assert not cfg.file.exists()
    qid = QuiltID(TEST_URL)
    cfg.save_uri(qid)
    assert cfg.file.exists()
    assert TEST_URL == cfg.get_uri()


def test_cfg_get_stage(cfg: QuiltConfig):
    assert not cfg.file.exists()
    p = cfg.write_file("test.txt", TEST_URL)
    filename = str(p)
    cfg.stage(filename, True)
    assert cfg.file.exists()
    stg = cfg.get_stage()
    assert stg is not None
    assert stg.get(filename) is not None
    assert stg[filename]["name"] == filename
    assert stg == cfg.get_stage(adds=True)
    assert stg != cfg.get_stage(adds=False)

    cfg.stage(filename, False)
    stg_rm = cfg.get_stage()
    assert stg_rm.get(filename) is not None
    assert stg_rm != cfg.get_stage(adds=True)
    assert stg_rm == cfg.get_stage(adds=False)
