from http import HTTPStatus


async def test_api_ping(api_client):
    resp = await api_client.get('/api/v1/ping')
    assert resp.status == HTTPStatus.OK
