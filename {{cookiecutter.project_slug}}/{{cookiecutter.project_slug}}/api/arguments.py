{%- set project_slug = cookiecutter.project_slug %}
import argparse
import os
import pwd

import configargparse
from aiomisc.log import LogFormat, LogLevel
from yarl import URL

from {{project_slug}}.utils.argparse import Environment, positive_int

parser = configargparse.ArgumentParser(
    allow_abbrev=False,
    auto_env_var_prefix="APP_API_",
    description="{{ cookiecutter.project_description }}",
    default_config_files=[
        os.path.join(
            os.path.expanduser("~"),
            ".config/{{ project_slug }}/api.conf"
        ),
        "/etc/{{ project_slug }}/api.conf",
    ],
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    ignore_unknown_config_file_keys=True,
)

parser.add_argument("-D", "--debug", action="store_true")
parser.add_argument(
    "-s", "--pool-size", type=int, default=4, help="Thread pool size"
)
parser.add_argument(
    "--forks", type=positive_int, default=4,
    help="Number of processes to spawn",
)

parser.add_argument(
    "-u", "--user", required=False,
    help="Change process UID", type=pwd.getpwnam
)

group = parser.add_argument_group("Logging options")
group.add_argument(
    "--log-level",
    default=LogLevel.info,
    choices=LogLevel.choices(),
)
group.add_argument(
    "--log-format",
    default=LogFormat.color,
    choices=LogFormat.choices(),
)

group = parser.add_argument_group("API Options")
group.add_argument("--api-address", default="127.0.0.1")
group.add_argument("--api-port", type=positive_int, default=8080)

group = parser.add_argument_group('Sentry options')
group.add_argument('--sentry-dsn', type=URL)
group.add_argument(
    '--sentry-env', choices=Environment.choices(), default=Environment.STAGE
)
