import asyncio
import logging
import os
from dataclasses import dataclass
from enum import unique, Enum
from gzip import GzipFile
from pathlib import Path
from subprocess import check_output
from tempfile import TemporaryFile

import aiohttp
import aiomisc
from aiomisc import threaded
from aiomisc.io import async_open
from yarl import URL

log = logging.getLogger()


@unique
class CompressionMode(Enum):
    SIMPLE = "SIMPLE"
    WHITESPACE_ONLY = "WHITESPACE_ONLY"


UNPKG_URL = URL("https://unpkg.com/")
VENDOR_PATH = Path("./vue_aiohttp/admin/static/vendor")


@dataclass(frozen=False)
class Resource:
    name: str
    path: str
    uglify: bool = False
    priority: int = 99
    directory: Path = Path("")
    site: URL = UNPKG_URL

    @property
    def filename(self) -> Path:
        return VENDOR_PATH / self.directory / self.name

    @property
    def url(self) -> URL:
        return self.site.with_path(self.path)


RESOURCES = (
    Resource(priority=10, name="jquery.js", path="jquery", uglify=True),
    Resource(
        priority=20,
        name="lodash.js",
        path="lodash@4.17.21/lodash.js",
        uglify=True,
    ),
    Resource(
        priority=20,
        name="wsrpc.js",
        path="@wsrpc/client@4.4.1/dist/wsrpc.js",
        uglify=True,
    ),
    Resource(
        priority=80, name="vue.js", path="vue@2.7.14/dist/vue.js", uglify=True
    ),
    Resource(
        priority=90,
        name="element-ui.js",
        path="element-ui@2.15.13/lib/index.js",
        uglify=True,
    ),
    Resource(
        priority=90,
        name="vue-router.js",
        path="vue-router@3.6.5/dist/vue-router.js",
        uglify=True,
    ),
    #####################
    Resource(
        name="element-icons.ttf",
        path="element-ui@2.15.13/lib/theme-chalk/fonts/element-icons.ttf",
        directory=Path("fonts"),
    ),
    Resource(
        name="element-icons.woff",
        path="element-ui@2.15.13/lib/theme-chalk/fonts/element-icons.woff",
        directory=Path("fonts"),
    ),
    ############################
    Resource(
        name="element-ui.css",
        uglify=False,
        path="element-ui@2.15.13/lib/theme-chalk/index.css",
    ),
)


async def collect() -> None:
    @threaded
    def ensure_path(resource: Resource) -> Path:
        resource.filename.parent.mkdir(exist_ok=True, parents=True)
        return resource.filename

    async with aiohttp.ClientSession(
        auto_decompress=True, raise_for_status=True
    ) as session:

        async def fetch_resource(resource: Resource) -> None:
            path = str(await ensure_path(resource))

            async with async_open(path, "wb+") as afp:
                async with session.get(resource.url) as response:
                    async for chunk in response.content.iter_any():
                        await afp.write(chunk)

            log.info("Downloading %s done", resource.url)

        await asyncio.gather(*map(fetch_resource, RESOURCES))

        @threaded
        def uglify() -> None:
            resources = sorted(
                filter(lambda x: x.uglify, RESOURCES), key=lambda x: x.priority
            )
            cmd = [
                "java",
                "-jar",
                "contrib/closure-compiler.jar",
                f"--compilation_level={CompressionMode.SIMPLE.value}",
            ]

            for resource in resources:
                cmd.append(f"--js={resource.filename}")

            out_file = str(VENDOR_PATH / "vendor.js")
            cmd.append(f"--js_output_file={out_file}")

            log.debug("Compilling %s", ' '.join(cmd))

            with TemporaryFile() as err:
                try:
                    log.info("Executing: %s", " ".join(cmd))
                    check_output(cmd, stderr=err)
                except:
                    err.seek(0)
                    log.error("Command output: %s", err.read())
                    raise

            log.info("Cleaning up pretty originals")
            for resource in resources:
                os.remove(str(resource.filename))

        await uglify()

        @threaded
        def compress_resource(resource_fname: str) -> None:
            with GzipFile(f"{resource_fname}.gz", "wb+") as gzfp:
                with open(f"{resource_fname}", "rb") as fp:
                    for chunk in iter(lambda: fp.read(65535), b""):
                        gzfp.write(chunk)

        await asyncio.gather(
            *[
                compress_resource(fname)
                for fname in VENDOR_PATH.rglob("*")
                if fname.is_file() and ".gz" not in fname.name
            ]
        )



def main() -> None:
    with aiomisc.entrypoint() as loop:
        loop.run_until_complete(collect())


if __name__ == '__main__':
    main()
