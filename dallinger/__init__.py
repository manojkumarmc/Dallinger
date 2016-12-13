"""This is Dallinger, a platform for simulating evolution with people."""

from . import (
    models,
    information,
    nodes,
    networks,
    processes,
    transformations,
    experiments,
    experiment_server,
    heroku
)

from localconfig import config
config.read("config.txt")

__all__ = (
    "config",
    "models",
    "information",
    "nodes",
    "networks",
    "processes",
    "transformations",
    "experiments",
    "heroku",
)
