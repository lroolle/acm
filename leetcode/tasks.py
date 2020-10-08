import logging

import datetime
import pymongo
import requests

from celery import Task, shared_task
from celery.utils.log import get_task_logger
from leetcode.requester import RequestException

from . import requester

logger = get_task_logger(__name__)


class MongoBaseTask(Task):
    queue = "mongo"
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 10}
    retry_backoff = True
    _db = None
    _db_name = ""

    @property
    def db(self):
        if self._db is None:
            # TODO: Add to config
            client = pymongo.MongoClient("localhost", 27017)
            self._db = client[self._db_name]
        return self._db


class LeetcodeMongoBaseTask(MongoBaseTask):
    _db_name = "leetcode"


class LeetcodeCNMongoBaseTask(MongoBaseTask):
    _db_name = "leetcode_cn"


class SessionBaseTask(Task):
    queue = "celery"
    autoretry_for = (
        AssertionError,
        RequestException,
    )
    retry_kwargs = {"max_retries": 10}
    retry_backoff = True
    _session = None
    _domain = ""

    @property
    def session(self):
        if self._session is None:
            session = requester.LeetCodeSession(only_domain=self._domain)
            self._session = session
        return self._session


class LeetcodeSessionBaseTask(SessionBaseTask):
    queue = "leetcode"
    _domain = "leetcode.com"


class LeetcodeCNSessionBaseTask(SessionBaseTask):
    # Do not share with leetcode.com for slow network when climbing GFW
    queue = "leetcodecn"
    _domain = "leetcode-cn.com"


@shared_task(bind=True, base=LeetcodeSessionBaseTask)
def get_problem_favorites_all_task(self) -> dict:
    favorites = requester.get_problem_favorites_all(self.session)
    return favorites


@shared_task(bind=True, base=LeetcodeCNSessionBaseTask)
def get_cn_problem_favorites_all_task(self) -> dict:
    favorites = requester.get_cn_problem_favorites_all(self.session)
    return favorites


@shared_task(bind=True, base=LeetcodeSessionBaseTask)
def get_problem_tags_all_task(self) -> dict:
    tags = requester.get_problem_tags_all(self.session)
    return tags


@shared_task(bind=True, base=LeetcodeCNSessionBaseTask)
def get_cn_problem_tags_all_task(self) -> dict:
    tags = requester.get_cn_problem_tags_all(self.session)
    return tags


@shared_task(bind=True, base=LeetcodeSessionBaseTask)
def get_problem_stats_all_task(self) -> dict:
    stats = requester.get_problem_stats_all(self.session)
    return stats


@shared_task(bind=True, base=LeetcodeCNSessionBaseTask)
def get_cn_problem_stats_all_task(self) -> dict:
    stats = requester.get_cn_problem_stats_all(self.session)
    return stats


@shared_task(bind=True, base=LeetcodeSessionBaseTask)
def get_problem_by_title_slug_task(self, title_slug: str) -> dict:
    problem = requester.get_problem_by_title_slug(self.session, title_slug)
    return problem


@shared_task(bind=True, base=LeetcodeCNSessionBaseTask)
def get_cn_problem_by_title_slug_task(self, title_slug: str) -> dict:
    problem = requester.get_cn_problem_by_title_slug(self.session, title_slug)
    return problem


@shared_task(bind=True, base=LeetcodeMongoBaseTask)
def leetcode_update_or_insert_mongo_task(self, collection_name, q={}, **kwargs):
    collection = self.db[collection_name]
    if q:
        collection.update_one(q, {"$set": kwargs}, upsert=True)
    else:
        collection.insert_one(kwargs)


@shared_task(bind=True, base=LeetcodeCNMongoBaseTask)
def leetcodecn_update_or_insert_mongo_task(self, collection_name, q={}, **kwargs):
    collection = self.db[collection_name]
    if q:
        collection.update_one(q, {"$set": kwargs}, upsert=True)
    else:
        collection.insert_one(kwargs)


@shared_task
def mongo_update_favorites_all_task(favorites, cn=False, collection_name="favorites"):
    if cn:
        mongo_task = leetcodecn_update_or_insert_mongo_task
    else:
        mongo_task = leetcode_update_or_insert_mongo_task

    for favorite in favorites:
        q = {"name": favorite["name"]}
        favorite.update({"update_time": datetime.datetime.now()})
        mongo_task.delay(collection_name=collection_name, q=q, **favorite)


@shared_task
def mongo_update_tags_all_task(tags, cn=False, collection_name="topic_tags"):
    if cn:
        mongo_task = leetcodecn_update_or_insert_mongo_task
    else:
        mongo_task = leetcode_update_or_insert_mongo_task

    topic_tags = tags.get("topics", [])
    for tag in topic_tags:
        q = {"slug": tag["slug"]}
        tag.update({"update_time": datetime.datetime.now()})
        mongo_task.delay(collection_name=collection_name, q=q, **tag)


@shared_task
def mongo_update_problem_stats_all_task(
    stats,
    cn=False,
    collection_name="problem_stats",
    history_collection_name="problem_stats_history",
):
    if cn:
        mongo_task = leetcodecn_update_or_insert_mongo_task
    else:
        mongo_task = leetcode_update_or_insert_mongo_task

    # A raw history  stats data include user current ac data
    update_time = datetime.datetime.now()
    stats.update(update_time=update_time)
    mongo_task.delay(collection_name=history_collection_name, q=None, **stats)

    problem_stats_pairs = stats.get("stat_status_pairs", [])
    for stat_item in problem_stats_pairs:
        stat = stat_item["stat"]
        q = {"question_id": stat["question_id"]}
        stat_data = {
            "update_time": update_time,
            "status": stat_item["status"],
            "difficulty_level": stat_item["difficulty"]["level"],
            "paid_only": stat_item["paid_only"],
            "is_favor": stat_item["is_favor"],
            "frequency": stat_item["frequency"],
            "progress": stat_item["progress"],
            "ac_rate": stat["total_acs"] / stat["total_submitted"],
            **stat,
        }

        mongo_task.delay(collection_name=collection_name, q=q, **stat_data)


@shared_task
def mongo_update_problem_task(problem, stat, cn=False, collection_name="problems"):
    if cn:
        mongo_task = leetcodecn_update_or_insert_mongo_task
    else:
        mongo_task = leetcode_update_or_insert_mongo_task

    # type(stat["question_id"]): int
    # type(problem["questionId"]): string  Eww... weirdo
    question_id = stat["stat"]["question_id"]
    problem.update(
        {
            "question_id": question_id,
            "update_time": datetime.datetime.now(),
            "stat": stat,
        }
    )
    q = {"questionId": problem["questionId"]}
    mongo_task.delay(collection_name=collection_name, q=q, **problem)


@shared_task
def mongo_update_problems_all_task(stats, cn=False, collection_name="problems"):
    if cn:
        get_problem_task = get_cn_problem_by_title_slug_task
    else:
        get_problem_task = get_problem_by_title_slug_task

    problem_stats_pairs = stats.get("stat_status_pairs", [])
    for stat_item in problem_stats_pairs:
        stat = stat_item["stat"]
        title_slug = stat_item["stat"]["question__title_slug"]
        flow = (
            get_problem_task.s(title_slug)
            | mongo_update_problem_task.s(
                stat=stat_item, cn=cn, collection_name=collection_name
            )
        )()
