# quiltplus
Resource-oriented API for Quilt's decentralized social knowledge platform

## Command-Line QuickStart

```bash
pip install quiltplus
qp get "quilt+s3://quilt-example#package=examples/echarts"
qp list
```

## Developmment

Uses the [trio](https://trio.readthedocs.io/en/stable/) version of Python's `async` I/O

```bash
git clone https://github.com/quiltdata/quiltplus
cd quiltplus
poetry self update
poetry install
export WRITE_BUCKET=writeable_s3_bucket
poetry run ptw --now .
```
## Pushing Changes
Be sure you to first set your [API token](https://pypi.org/manage/account/) using `poetry config pypi-token.pypi <pypi-api-token>`

```bash
# merge PR
poetry version patch # minor major
poetry build
poetry publish
# create new branch
poetry version prepatch # preminor premajor
```
