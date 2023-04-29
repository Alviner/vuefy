from http import HTTPStatus

from {{cookiecutter.project_slug}} import __version__
from {{cookiecutter.project_slug}}.admin.handlers.v1.ping import X_VERSION


URL = '/api/v1/ping'


async def test_version(api_client):
    resp = await api_client.get(URL)
    assert resp.status == HTTPStatus.OK
    assert resp.headers[X_VERSION] == __version__
