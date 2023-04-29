from logging import getLogger

from pydantic import BaseModel
from wsrpc_aiohttp import Route, decorators

from {{cookiecutter.project_slug}}.utils.argparse import Environment


log = getLogger(__name__)


class EnvModel(BaseModel):
    environment: Environment


class EnvHandler(Route):

    @decorators.proxy
    async def load(self) -> BaseModel:
        return EnvModel(
            environment=self.socket.request.app['env']  # type: ignore
        )
