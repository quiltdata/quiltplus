from .conftest import *

WRITE_URL = None
WRITE_BKT = "quilt-ernest-staging"
TIMESTAMP = int(round(time.time()))
WRITE_URL = f"quilt+s3://{WRITE_BKT}#package=test/{TIMESTAMP}"

if not WRITE_URL:
    pytest.skip("no writeable bucket available", allow_module_level=True)


@pytest.fixture
def pkg():
    return QuiltPackage.FromURI(WRITE_URL)


async def test_push_browse_exception(pkg):
    with pytest.raises(Exception) as e_info:
        assert await pkg.quilt()


async def test_push(pkg):
    assert pkg is not None


# Init Empty Package


# Create new Package

# Read that Package

# Update Package

# Verify Result
