from asyncio import gather
import logging
import json
from http import HTTPStatus

from aiohttp import web, web_exceptions
from aiomisc import timeout

from {{cookiecutter.project_slug}} import __version__
from {{cookiecutter.project_slug}}.admin.handlers import BaseHandler


X_VERSION = 'X-VERSION'


log = logging.getLogger(__name__)


class PingHandler(BaseHandler):

    # FIXME: Add checks
    async def _check_db(self) -> bool:
        try:
            # make select 1
            return True
        except Exception:
            log.exception("Failed to ping db")
            return False

    @timeout(5)
    async def get(self) -> web.Response:
        # TODO: Check dependencies
        ok_db = await gather(
            *[self._check_db()]
        )

        status = all([ok_db])

        status_code = HTTPStatus.OK
        if not status:
            raise web_exceptions.HTTPInternalServerError

        return web.json_response(
            data={'status': status, 'db': ok_db},
            status=status_code,
            headers={X_VERSION: __version__},
            dumps=json.dumps,
        )
