# Init logging config
# TODO: mkdir(logs) or handlers may config failed

try:
    from . import config_private as config
except ImportError:
    print("You may want a private config by `cp config_default.py config_private.py`")
    from . import config_default as config

from . import log_config
from . import celery

__all__ = ["celery.celery_app"]
