sinclude .env # create from example.env
PROJECT=quiltplus
.PHONY: install test watch all clean

TEST_README=--codeblocks
ifeq ($(TEST_OS),windows-latest)
	TEST_README=''
endif

all: install update test

clean:
	rm -rf coverage_html
	rm -f coverage*
	rm -f .coverage*
	rm -rf quiltplus/.pytest_cache

install:
	poetry install

update:
	poetry update

test: typecheck
	echo "Testing with WRITE_BUCKET=$(WRITE_BUCKET)"
	poetry run pytest $(TEST_README) --cov --cov-report xml:coverage.xml

test-short:
	make test "SKIP_LONG_TESTS=True"

test-long:
	make test "SKIP_LONG_TESTS=False"

typecheck:
	poetry run mypy $(PROJECT) tests

coverage:
	echo "Using WRITE_BUCKET=$(WRITE_BUCKET) | SKIP_LONG_TESTS=$(SKIP_LONG_TESTS)"
	poetry run pytest --cov --cov-report html:coverage_html
	open coverage_html/index.html

watch:
	poetry run ptw --now .

tag:
	git tag `poetry version | awk '{print $$2}'`
	git push --tags

pypi: clean clean-git
	poetry version
	poetry build
	poetry publish --dry-run
	echo "poetry version prepatch" # major minor

clean-git:
	git branch | grep -v '*' | grep -v 'main' | xargs git branch -D

which:
	which $(PROJECT)
	$(PROJECT) --version

pip-install:
	python3 -m pip install $(PROJECT)
	make which

pip-upgrade:
	python3 -m pip install --upgrade $(PROJECT)
	make which

pip-update:
	poetry self update
	python3 -m pip install --upgrade pip


