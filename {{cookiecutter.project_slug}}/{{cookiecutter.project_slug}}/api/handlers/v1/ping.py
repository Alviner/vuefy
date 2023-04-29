import logging
from asyncio import gather
from http import HTTPStatus

import json
from aiohttp import web, web_exceptions
from aiomisc import timeout

log = logging.getLogger(__name__)


class PingHandler(web.View):

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
            dumps=json.dumps,
        )
