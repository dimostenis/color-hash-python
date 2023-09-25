.PHONY: install-pip-tools reqs install-env env test tag build publish

VERSION := $(shell python -c 'import colorhash;print(colorhash.__version__)')

# dev option to create update whole venv
env: install-pip-tools reqs install-env

build:
	hatch build

# get current version and set a tag
tag:
	git tag -f v$(VERSION)

# push both commits and tags
push:
	git push
	git push -f --tags

# https://test.pypi.org/project/colorhash/
publish-test: check
	twine upload --config-file .pypirc --repository testpypi dist/*$(VERSION)*

# https://pypi.org/project/colorhash/
publish: check
	twine upload --config-file .pypirc --repository pypi dist/**$(VERSION)*

# ===================
# --- SUB TARGETS ---
# ===================

install-pip-tools:
	pip install -U pip pip-tools

reqs:
	rm -f requirements-dev.txt
	pip-compile --extra=dev --output-file=requirements-dev.txt pyproject.toml

install-env:
	pip-sync requirements-dev.txt

test:
	hatch run test:test

check:
	twine check dist/*
