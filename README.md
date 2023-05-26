# quiltplus

Resource-oriented API for Quilt's decentralized social knowledge platform

API-only. For command-line invocation, see [udc](https://pypi.org/project/udc/).

## Command-Line QuickStart

```bash
python3 -m pip install quiltplus # or
python3 -m pip install --upgrade quiltplus
```

## Developmment

Uses [anyio](https://github.com/agronholm/anyio)
to support Python's `async/await` via either
[trio](https://trio.readthedocs.io/en/stable/) or
[asyncio](https://docs.python.org/3/library/asyncio.html).

<!--pytest.mark.skip-->
```bash
git clone https://github.com/quiltdata/quiltplus
cd quiltplus
poetry self update
poetry install
export WRITE_BUCKET=writeable_s3_bucket
poetry run pytest --cov-report html && open htmlcov/index.html # make coverage
poetry run ptw --now . # make watch
```

## Pushing Changes

Be sure you to first set your [API token](https://pypi.org/manage/account/) using `poetry config pypi-token.pypi <pypi-api-token>`

<!--pytest.mark.skip-->
```bash
# merge PR
poetry version patch # minor major
poetry build
poetry publish
# create new branch
poetry version prepatch # preminor premajor
```
