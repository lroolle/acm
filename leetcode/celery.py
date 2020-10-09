from datetime import timedelta

import celery
from celery.schedules import crontab


celery_app = celery.Celery("leetcode")


class CeleryConfig(object):
    broker_url = "redis://127.0.0.1:6379/8"
    result_backend = "redis://127.0.0.1:6379/7"
    # result_backend = "mongodb://localhost:27017/"

    task_ignore_result = False
    # task_store_errors_even_if_ignored = True
    timezone = "Asia/Shanghai"

    # beat_schedule = {
    #     "update_all_problems_task": {
    #         "task": "",
    #         "schedule": crontab(minute=0, hour=23),
    #     },
    # }


celery_app.config_from_object(CeleryConfig)
celery_app.autodiscover_tasks(["leetcode.tasks", "leetcode.test_tasks"])
