{%- set project_slug = cookiecutter.project_slug %}
{%- set project_namespace = cookiecutter.project_namespace %}
PROJECT_PATH := {{ project_slug }}

VERSION = $(shell poetry version -s)

CI_REGISTRY ?= ghcr.io
CI_PROJECT_NAMESPACE ?= {{ project_namespace }}
CI_PROJECT_NAME ?= $(shell echo $(PROJECT_PATH) | tr -cd "[:alnum:]")
CI_REGISTRY_IMAGE ?= $(CI_REGISTRY)/$(CI_PROJECT_NAMESPACE)/$(CI_PROJECT_NAME)
DOCKER_TAG = $(shell echo $(VERSION) | tr '+' '-')

all:
	@echo "make build 		- Build a docker image"
	@echo "make lint 			- Syntax check python with ruff and mypy"
	@echo "make pytest 		- Test this project"
	@echo "make format 		- Format project with gray"
	@echo "make upload 		- Upload this project to the docker-registry"
	@echo "make clean 		- Remove files which creates by distutils"
	@echo "make purge 		- Complete cleanup the project"
	@exit 0

wheel:
	poetry build -f wheel

build: clean wheel
	docker build -t $(CI_REGISTRY_IMAGE):$(DOCKER_TAG) --target release .

clean:
	rm -fr dist

clean-pyc:
	find . -iname '*.pyc' -delete

lint:
	poetry run mypy $(PROJECT_PATH)
	poetry run ruff $(PROJECT_PATH) tests


format:
	poetry run gray $(PROJECT_PATH) tests
	poetry run ruff $(PROJECT_PATH) tests --fix
	yarn lint-fix

purge: clean
	rm -rf ./.venv

pytest:
	poetry run pytest

local:
	docker-compose -f docker-compose.dev.yml up --force-recreate --renew-anon-volumes --build

pytest-ci:
	poetry run pytest -v --cov $(PROJECT_PATH) --cov-report term-missing --disable-warnings --junitxml=report.xml
	poetry run coverage xml

upload: build
	docker push $(CI_REGISTRY_IMAGE):$(DOCKER_TAG)

develop: clean
	poetry -V
	poetry install
	yarn install

build-vendor:
	yarn build
