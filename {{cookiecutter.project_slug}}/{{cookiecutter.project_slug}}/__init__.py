try:
    from importlib.metadata import Distribution
    __version__ = Distribution.from_name("{{ cookiecutter.project_slug }}").version
except ImportError:
    __version__ = "0.0.0"
