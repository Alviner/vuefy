from http import HTTPStatus

import pytest


@pytest.mark.parametrize('path', ['/', '/other/page'])
async def test_vue_router_middleware(path: str, api_client):
    async with api_client.get(path) as resp:
        assert resp.status == HTTPStatus.OK
        body = await resp.text()
        assert '<div id="app">' in body


async def test_static_file(api_client):
    async with api_client.get('/static/main.js') as resp:
        assert resp.status == HTTPStatus.OK
        body = await resp.text()
        assert 'createApp' in body


async def test_not_found_static_file(api_client):
    async with api_client.get('/static/wrong') as resp:
        assert resp.status == HTTPStatus.NOT_FOUND
