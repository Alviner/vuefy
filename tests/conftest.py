import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

import pytest as pytest
from cookiecutter.main import cookiecutter

TEMPLATE_PATH = Path(__file__).parent.parent


@pytest.fixture(autouse=True, scope='session')
def ci_env():
    env = {
        k: os.environ.pop(k) for k in os.environ if k.startswith("CI_")
    }
    try:
        yield env
    finally:
        os.environ.update(env)


@pytest.fixture(scope='session')
def tmpdir():
    @contextmanager
    def _getter(dir: Optional[Path] = None, prefix: Optional[str] = None):
        with tempfile.TemporaryDirectory(dir=dir, prefix=prefix) as dirname:
            yield dirname

    return _getter


@pytest.fixture(scope='session')
def project_root(tmpdir):
    with tmpdir(
        prefix="projects_"
    ) as dirname:
        yield dirname


@pytest.fixture
def project_path(tmpdir, project_root):
    with tmpdir(dir=project_root) as dirname:
        yield dirname


@pytest.fixture
def project(project_path):
    project = cookiecutter(
        template=str(TEMPLATE_PATH),
        no_input=True,
        output_dir=str(project_path),
    )
    return project
