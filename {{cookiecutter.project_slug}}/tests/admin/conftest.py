from argparse import Namespace

import pytest
from aiohttp import hdrs, web
from aiohttp.test_utils import TestClient, TestServer
from wsrpc_aiohttp import WSRPCClient
from yarl import URL

from {{cookiecutter.project_slug}}.admin.__main__ import parser
from {{cookiecutter.project_slug}}.admin.services.rest import REST



@pytest.fixture
def services(arguments, rest_service):
    return [
        rest_service,
    ]


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
def arguments(rest_url: URL):
    return parser.parse_args(
        [
            '--log-level=debug',
            f'--api-address={rest_url.host}',
            f'--api-port={rest_url.port}'
        ]
    )


@pytest.fixture
async def rest_service(arguments: Namespace):
    return REST(
        address=arguments.api_address,
        port=arguments.api_port,
        debug=arguments.debug,
        env=arguments.sentry_env,
    )


@pytest.fixture()
async def api_client(rest_url):
    server = TestServer(web.Application())
    server._root = rest_url
    client = TestClient(server)
    try:
        yield client
    finally:
        await client.close()


@pytest.fixture
async def wsrpc_client(rest_url, services):
    client = WSRPCClient(
        rest_url.with_path('ws/').with_scheme('ws'),
        headers={hdrs.ORIGIN: str(rest_url)},
    )
    try:
        await client.connect()
        yield client
    finally:
        await client.close()
