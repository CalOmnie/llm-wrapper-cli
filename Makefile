.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint lint/flake8

.DEFAULT_GOAL := help

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint/flake8: ## check style with flake8
	flake8 llm_cli tests


lint: lint/flake8 ## check style

test: ## run tests quickly with the default Python
	pytest --cov=llm_cli --cov-report term-missing:skip-covered tests/

coverage: ## check code coverage quickly with the default Python
	coverage run --source llm_wrapper_cli setup.py test
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html


release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python -m build

install: clean ## install the package to the active Python's site-packages
	pip install -e .
