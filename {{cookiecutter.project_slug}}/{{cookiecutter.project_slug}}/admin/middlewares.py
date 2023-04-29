from aiohttp.typedefs import Handler
from aiohttp.web_middlewares import middleware
from aiohttp.web_request import Request
from aiohttp.web_response import StreamResponse
from aiohttp.web_urldispatcher import MatchInfoError


@middleware
async def vue_router_middleware(
    request: Request, handler: Handler,
) -> StreamResponse:
    if isinstance(await request.app.router.resolve(request), MatchInfoError):
        request = request.clone(rel_url='/')
        info = await request.app.router.resolve(request)
        return await info.handler(request)
    return await handler(request)
