{%- set project_name = cookiecutter.project_name.capitalize() %}
{%- set project_slug = cookiecutter.project_slug %}

# {{ project_name }}

{{ cookiecutter.project_description }}

## How to develop

- `make develop` - create virtualenv, install develop package,
- `make pytest` - run pytest
- `make lint` - run ruff with mypy
- `poetry run {{ project_slug }}_admin` - start admin service locally
- `poetry run {{ project_slug }}_api` - start api service locally
