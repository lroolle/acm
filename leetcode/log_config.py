import os
from logging.config import dictConfig

# Make sure log dir exists
if not os.path.exists("logs"):
    os.mkdir("logs")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(levelname)07s: %(message)s"},
        "verbose": {
            "format": "[%(asctime)s: %(levelname)s/%(filename)s-%(lineno)s:%(funcName)s] %(message)s"
        },
    },
    "handlers": {
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "monger_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/monger.log",
            "formatter": "verbose",
        },
        "leetcode_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/leetcode.log",
            "formatter": "verbose",
        },
        "celery_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/celery.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "leetcode.requester": {
            "handlers": ["console", "leetcode_file",],
            "propagate": False,
            "level": "DEBUG",
        },
        "leetcode.requester.LeetCodeSession": {
            "handlers": ["console", "leetcode_file",],
            "propagate": False,
            "level": "DEBUG",
        },
        "leetcode.monger": {
            "handlers": ["console", "monger_file",],
            "propagate": False,
            "level": "DEBUG",
        },
        "leetcode.tasks": {
            "handlers": ["console", "celery_file",],
            "propagate": False,
            "level": "DEBUG",
        },
    },
}

dictConfig(LOGGING)
