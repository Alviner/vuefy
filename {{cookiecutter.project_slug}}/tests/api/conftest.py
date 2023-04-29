{%- set project_slug = cookiecutter.project_slug -%}
import pytest
from aiohttp.test_utils import TestClient, TestServer
from aiohttp.web_app import Application
from yarl import URL

from {{ project_slug }}.api.__main__ import parser
from {{ project_slug }}.api.services.rest import REST


@pytest.fixture
def rest_port(aiomisc_unused_port_factory):
    return aiomisc_unused_port_factory()


@pytest.fixture
def rest_url(rest_port, localhost) -> URL:
    return URL.build(
        scheme='http',
        host=localhost,
        port=rest_port
    )


@pytest.fixture
def arguments(rest_url):
    return parser.parse_args([
        '--log-level=debug',
        f'--api-address={rest_url.host}',
        f'--api-port={rest_url.port}',
    ])


@pytest.fixture
async def rest_service(arguments):
    return REST(
        address=arguments.api_address,
        port=arguments.api_port,
    )


@pytest.fixture
def services(arguments, rest_service):
    return [rest_service]


@pytest.fixture()
async def api_client(rest_url):
    server = TestServer(Application())
    server._root = rest_url

    client = TestClient(server)
    try:
        yield client
    finally:
        await client.close()
