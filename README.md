# quiltplus
Resource-oriented API for Quilt's decentralized social knowledge platform

As of v0.4.0 all Resources are fetched sing the [trio](https://trio.readthedocs.io/en/stable/) version of `async`

# Developmment
## Setup

```
git clone https://github.com/quiltdata/quiltplus
cd quiltplus
poetry self update
poetry install
poetry run pytest-watch
```
## Pushing Changes
Be sure you to first set your [API token](https://pypi.org/manage/account/) using `poetry config pypi-token.pypi <pypi-api-token>`
```
# merge PR
poetry version patch # minor major
poetry build
poetry publish
# create new branch
poetry version prepatch # preminor premajor
```
