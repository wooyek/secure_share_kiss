# This will read missing environment variables from a file
# We want to do this before loading any base settings as they may depend on environment
# Do
from pathlib import Path

from environ import environ

environment_config = Path(__file__).with_suffix('.env')
if environment_config.exists():
    environ.Env.read_env(str(environment_config))

# noinspection PyUnresolvedReferences
from .settings import *  # noqa: F402, F403, F401 isort:skip

