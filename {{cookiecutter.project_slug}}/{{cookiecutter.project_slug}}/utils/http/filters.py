import logging
import re
from typing import Any

from aiohttp.log import access_logger


class PingFilter(logging.Filter):
    REGEX_PING = re.compile(r'^GET /api/v[0-9]+/ping ')

    def filter(self, record: Any) -> bool:
        return self.REGEX_PING.search(record.first_request_line) is None


def config_filters() -> None:
    access_logger.addFilter(PingFilter())
