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


async def test_push_unbrowsable_new(pkg: QuiltPackage):
    with pytest.raises(Exception) as e_info:
        assert await pkg.quilt()


async def test_push(pkg: QuiltPackage):
    print(WRITE_URL)
    assert pkg is not None

    # Create new Package
    pkg.write_text(f"# Hello World!\n{TIMESTAMP}", 'README.md')
    qpkg = await pkg.put('README')
    assert qpkg is not None

# Read that Package
    files = await pkg.list()
    assert 'README.md' in files

# Update Package
    pkg.write_text(f"# Goodbye Cruel World!\n{TIMESTAMP}", 'WRITEME.md')
    q_local = await pkg.local()
    print(q_local)
    q_local.browse(pkg.name, registry=pkg.registry)
    result = q_local.push(pkg.name, registry=pkg.registry, message='direct WRITEME')

    #qpkg2 = await pkg.put('WRITEME')
    #assert qpkg2 is not None

# Verify Result
