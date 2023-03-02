# quiltplus

Resource-oriented API for Quilt's decentralized social knowledge platform

## Command-Line QuickStart

```bash
pip install quiltplus
qp -U "quilt+s3://quilt-example#package=examples/echarts" pkg # get
qp list
qp --help
```

### Detailed Command-Line

```bash
export WRITE_BUCKET=writeable_s3_bucket
# create empty package and save to config
qp -U "quilt+s3://$(WRITE_BUCKET)#package=test/quiltplus" pkg -x post
time > README.md
qp stage -a README.md
qp stage # displays staged files
qp pkg -x patch # uploads staged files
```

## Developmment

Uses the [trio](https://trio.readthedocs.io/en/stable/) version of Python's `async` I/O

```bash
git clone https://github.com/quiltdata/quiltplus
cd quiltplus
poetry self update
poetry install
export WRITE_BUCKET=writeable_s3_bucket
poetry run pytest --cov-report html && open htmlcov/index.html
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
