import logging

from celery import Task, shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class LeetcodeBaseTask(Task):
    queue = "leetcode"
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 10}
    retry_backoff = True


class LeetcodeCnBaseTask(Task):
    # Do not share with leetcode.com for slow climbing GFW
    queue = "leetcodecn"
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 10}
    retry_backoff = True
