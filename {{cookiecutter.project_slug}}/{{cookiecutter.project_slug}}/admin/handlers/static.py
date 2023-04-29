import hashlib
import logging
import os
from functools import lru_cache
from pathlib import Path

from aiohttp import hdrs, web
from aiomisc import threaded


log = logging.getLogger(__name__)


@lru_cache(2048)
def _hash_file_content(  # type: ignore
    fname: str, chunk_size: int = 65535, *_,
) -> str:
    hashsum = hashlib.md5()

    with open(fname, 'rb') as fp:
        for chunk in iter(lambda: fp.read(chunk_size), b''):
            hashsum.update(chunk)

    return hashsum.hexdigest()


@threaded
def hash_file_content(  # type: ignore
    fname: str, chunk_size: int = 65535, *args,
) -> str:
    return _hash_file_content(fname, chunk_size, *args)


class StaticResource(web.StaticResource):
    @threaded
    def file_info(self, fname: str) -> os.stat_result:
        if not os.path.isfile(fname):
            raise FileNotFoundError

        return os.stat(fname)

    async def _handle(self, request: web.Request) -> web.StreamResponse:

        directory = Path(self._directory)
        filename = request.match_info['filename']
        file_path = (directory / filename).resolve()
        if directory not in file_path.parents:
            log.error(
                'Not serving file %r because it is outside static '
                'file directory %r (got filename %r)',
                file_path,
                directory,
                filename,
            )
            raise web.HTTPNotFound

        if (gzip_file := file_path.with_name(file_path.name + '.gz')).is_file():
            file_path = gzip_file

        real_fname = str(file_path)

        try:
            info = await self.file_info(file_path)
        except FileNotFoundError:
            log.error('file not found')
            raise web.HTTPNotFound

        etag = await hash_file_content(
            real_fname,
            self._chunk_size,
            info.st_size,
            info.st_atime,
            info.st_mtime,
            info.st_ctime,
            info.st_mode,
        )

        etag = f'W/"{etag}"'

        if request.headers.get(hdrs.IF_NONE_MATCH, '') == etag:
            raise web.HTTPNotModified

        response = web.FileResponse(file_path)
        response.headers[
            hdrs.CACHE_CONTROL
        ] = 'must-revalidate, max-age=0'
        response.headers[hdrs.ETAG] = etag

        return response
