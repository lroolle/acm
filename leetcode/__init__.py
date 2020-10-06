# Init logging config
# TODO: mkdir(logs) or handlers may config failed
from . import logging
from . import celery

try:
    from . import config_private as config
except ImportError:
    print("You may want a private config by `cp config_default.py config_private.py`")
    from . import config_default as config

__all__ = ["celery.celery_app"]
