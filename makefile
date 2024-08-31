SOURCE_DIR = pytomation
TEST_DIR = tests
PROJECT_DIRS = $(SOURCE_DIR) $(TEST_DIR)
PWD := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
PROJECT_VERSION ?= v$(shell poetry version -s)
PROJECT_NAME ?= pytomation
PYTHON_VERSION ?= $(shell cat .python-version)


init:
	poetry install

lint:
	poetry run pre-commit run --all-files

test:
	poetry run pytest --cov=$(SOURCE_DIR) $(TEST_DIR)

ci-test:
	poetry run pytest --cov-report xml:report/coverage.xml --cov=$(SOURCE_DIR) --junit-xml=report/test.xml $(TEST_DIR)

build:
	poetry build -n

version:
	@echo "Available rules: patch, minor, major, prepatch, preminor, premajor, prerelease"
	@read -p "Specify the sem version rule: " rule; \
	poetry version $$rule

test-tag:
	@echo "My version: $(shell poetry version)"
	git tag "dev$(shell poetry version -s)"

tag:
	@echo "My version: $(shell poetry version)"
	git tag -a "v$(shell poetry version -s)" -m

info:
	@echo "Project name: ${PROJECT_NAME}"
	@echo "Project version: ${PROJECT_VERSION}"
	@echo "Python version: ${PYTHON_VERSION}"
