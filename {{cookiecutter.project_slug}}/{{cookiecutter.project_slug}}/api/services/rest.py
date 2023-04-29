import logging
from typing import Any, Tuple

from aiohttp import web
from aiomisc.service.aiohttp import AIOHTTPService

from {{cookiecutter.project_slug}}.api.handlers.v1.ping import PingHandler

log = logging.getLogger(__name__)

MEGABYTE = 1024 ** 2

HandlersType = Tuple[Tuple[str, str, Any], ...]


class REST(AIOHTTPService):
    ROUTES: HandlersType = (
        ("GET", "/api/v1/ping", PingHandler),
    )

    async def create_application(self) -> web.Application:
        app = web.Application(client_max_size=10 * MEGABYTE)
        for method, path, handler in self.ROUTES:
            app.router.add_route(method, path, handler)
        return app
