.PHONY: init test lint pretty

BIN = .venv/bin/
CODE = soccerdata
PY = 3.9

init:
	python3 -m venv .venv
	poetry install

test:
	nox -rs tests-$(PY) -- $(args)

mypy:
	nox -rs mypy-$(PY) -- $(args)

lint:
	nox -rs pre-commit -- $(args)

precommit_install:
	nox -rs pre-commit -- install

bump_major:
	$(BIN)bumpversion major

bump_minor:
	$(BIN)bumpversion minor

bump_patch:
	$(BIN)bumpversion patch

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
