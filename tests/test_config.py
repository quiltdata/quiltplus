from .conftest import *

RM_LOCAL = os.path.join(QuiltConfig.CONFIG_FOLDER, QuiltConfig.REVISEME_FILE)


@pytest.fixture
def cfg():
    with TemporaryDirectory() as tmpdirname:
        config = QuiltConfig(Path(tmpdirname))
        logging.debug(config)
        yield config


def test_cfg_as():
    assert f"]\nURL={TEST_URL}" in QuiltConfig.AsShortcut(TEST_URL)
    assert f'{{ URL = "{TEST_URL}"; }}' in QuiltConfig.AsWebloc(TEST_URL)
    assert f"packages:\n- {TEST_URL}" in QuiltConfig.AsPackages(TEST_URL)


def test_cfg_fixture(cfg: QuiltConfig):
    assert cfg


def test_cfg_write(cfg: QuiltConfig):
    p = cfg.write_config("test.txt", TEST_URL)
    assert QuiltConfig.CONFIG_FOLDER in str(p)
    assert "test.txt" in str(p)
    assert TEST_URL == p.read_text()


def test_cfg_save_webloc(cfg: QuiltConfig):
    p = cfg.save_webloc("test2.webloc", TEST_URL)
    assert QuiltConfig.CONFIG_FOLDER in str(p)
    assert "test2.webloc" in str(p)
    assert f'{{ URL = "{TEST_URL}"; }}' in p.read_text()

    files = cfg.list_config()
    assert "test2.webloc" in files
    assert "test2.URL" in files


def test_cfg_save_config(cfg: QuiltConfig):
    qid = QuiltID(TEST_URL)
    configs = cfg.save_config(qid)
    assert QuiltConfig.CONFIG_YAML in configs
    files = cfg.list_config()
    for cf in configs:
        assert cf in files

    p = cfg.path / QuiltConfig.CONFIG_YAML
    assert f"packages:\n- {TEST_URL}" in p.read_text()
