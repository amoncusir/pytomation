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
	poetry run pytest $(TEST_DIR)

info:
	@echo "Project name: ${PROJECT_NAME}"
	@echo "Project version: ${PROJECT_VERSION}"
	@echo "Python version: ${PYTHON_VERSION}"
