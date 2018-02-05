import logging

logger = logging.getLogger('jobs')

from config import config
from .buy import Buy

__all__ = ['jobs_all', 'logger']

jobs_mobile = []
jobs_web = [Buy]
jobs_all = jobs_mobile + jobs_web


def set_logger():
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(config.log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


set_logger()
