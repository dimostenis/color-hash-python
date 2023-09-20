.PHONY: install-pip-tools reqs install-env env test tag build publish

# dev option to create update whole venv
env: install-pip-tools reqs install-env

build:
	hatch build

# https://test.pypi.org/project/colorhash/
publish-test: check
	twine upload --config-file .pypirc --repository testpypi dist/*

# https://pypi.org/project/colorhash/
publish: check
	twine upload --config-file .pypirc --repository pypi dist/*

# get current version and set a tag
tag:
	git tag -f v$(shell python -c 'import colorhash;print(colorhash.__version__)')

# push both commits and tags
push:
	git push
	git push -f --tags

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
