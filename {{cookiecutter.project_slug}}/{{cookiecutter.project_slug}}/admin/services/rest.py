{%- set project_slug = cookiecutter.project_slug %}
import logging
from itertools import chain
from typing import Any, Tuple

from aiohttp import web
from aiohttp.web_app import Application
from aiomisc.service.aiohttp import AIOHTTPService
from wsrpc_aiohttp import WebSocketAsync

from {{project_slug}}.admin import STATIC_ROOT
from {{project_slug}}.admin.handlers.index import IndexHandler
from {{project_slug}}.admin.handlers.static import StaticResource
from {{project_slug}}.admin.handlers.v1.ping import PingHandler
from {{project_slug}}.admin.handlers.ws.env import EnvHandler
from {{project_slug}}.admin.middlewares import vue_router_middleware
from {{project_slug}}.admin.utils.serializers import config_serializers
from {{project_slug}}.utils.argparse import Environment


log = logging.getLogger(__name__)

ApiHandlersType = Tuple[Tuple[str, str, Any], ...]
WsHandlersType = Tuple[Tuple[str, Any], ...]


class REST(AIOHTTPService):
    __required__ = ('env',)

    env: Environment

    _middlewares = (vue_router_middleware,)
    __dependencies__: Tuple[str, ...] = tuple()

    API_ROUTES: ApiHandlersType = (
        ('GET', '/', IndexHandler),
        ('GET', '/api/v1/ping', PingHandler),

    )

    WS_ROUTES: WsHandlersType = (
        ('env', EnvHandler),
    )

    async def create_application(self) -> Application:
        config_serializers()
        app = web.Application()

        self._add_routes(app)
        self._add_middlewares(app)
        self._set_dependencies(app)
        return app

    def _add_routes(self, app: Application) -> None:
        for method, path, handler in self.API_ROUTES:
            app.router.add_route(
                method=method,
                path=path,
                handler=handler,
            )
        app.router.add_route('*', '/ws/', WebSocketAsync)
        for route, handler in self.WS_ROUTES:
            WebSocketAsync.add_route(
                route=route, handler=handler,
            )

        app.router.register_resource(
            StaticResource('/static', STATIC_ROOT)
        )

    def _set_dependencies(self, app: Application) -> None:
        for name in chain(self.__required__, self.__dependencies__):
            app[name] = getattr(self, name)

    def _add_middlewares(self, app: web.Application) -> None:
        for middleware in self._middlewares:
            app.middlewares.append(middleware)
