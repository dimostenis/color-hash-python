VERSION := $(shell python -c 'import colorhash;print(colorhash.__version__)')

# dev option to create update whole venv (installs colorhash too)
.PHONY: setup
setup:
	pre-commit autoupdate
	pre-commit install
	rm uv.lock
	uv lock
	uv sync --all-extras
	hatch env prune
	hatch env create

# -------------------
# PUBLISH NEW VERSION
# -------------------

# 0. :: Usual pre-requisites
# - new branch
# - bump version in pyproject.toml
# - code

# 1. :: Test it
.PHONY: test
test:
	hatch run test:test

# 2. :: Build into /dist
.PHONY: build
build:
	hatch build

# 3. Check pkg/whl if its OK
.PHONY: check
check:
	twine check dist/*

# 4. :: Commit changes

# 5. :: Tag final (in this release) commit
tag:
	git tag -f v$(VERSION)

# 6. :: Push both commits and tags
.PHONY: push
push:
	git push
	git push -f --tags

# 7. :: Publish latest version to PyPI test index
# https://test.pypi.org/project/colorhash/
.PHONY: publish-test
publish-test: check
	twine upload --config-file .pypirc --repository testpypi dist/*$(VERSION)*

# 8. :: Publish latest version to PyPI
# https://pypi.org/project/colorhash/
.PHONY: publish
publish: check
	twine upload --config-file .pypirc --repository pypi dist/*$(VERSION)*

# 9. :: Create new Release on GitHub
# https://github.com/dimostenis/color-hash-python/releases/new

# -------------------

# generates README markdown tables and color tiles
.PHONY: docs
docs:
	python -m docs.gen
