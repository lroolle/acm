import datetime
import pymongo
import requests

from celery import Task, shared_task, chord
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
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
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


# Leetcode & Leetcode-cn Request Problems Tasks
@shared_task(bind=True, base=LeetcodeSessionBaseTask)
def submit_problem_task(
    self, slug: str, frontend_id: str, lang: str, code: str
) -> dict:
    submission_id = requester.submit_problem(
        self.session, slug, frontend_id, lang, code
    )
    return submission_id


@shared_task(bind=True, base=LeetcodeCNSessionBaseTask)
def submit_cn_problem_task(
    self, slug: str, frontend_id: str, lang: str, code: str
) -> dict:
    submission_id = requester.submit_cn_problem(
        self.session, slug, frontend_id, lang, code
    )
    return submission_id


@shared_task(bind=True, base=LeetcodeSessionBaseTask)
def submission_check_task(self, submission_id: int) -> dict:
    result = requester.submission_check(self.session, submission_id)
    return result


@shared_task(bind=True, base=LeetcodeCNSessionBaseTask)
def submission_check_cn_task(self, submission_id: int) -> dict:
    result = requester.submission_check_cn(self.session, submission_id)
    return result


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


# CN Request Solutions Tasks
@shared_task(bind=True, base=LeetcodeCNSessionBaseTask)
def get_cn_solution_tags_task(self, problem_slug: str) -> dict:
    solution_tags = requester.get_cn_solution_tags_list(self.session, problem_slug)
    return solution_tags


@shared_task(bind=True, base=LeetcodeCNSessionBaseTask)
def get_cn_solution_list_task(self, problem_slug: str, limit=10) -> dict:
    solution_list = requester.get_cn_solution_list(
        self.session, problem_slug, limit=limit
    )
    return solution_list


@shared_task(bind=True, base=LeetcodeCNSessionBaseTask)
def get_cn_solution_detail_article_task(self, article_slug: str) -> dict:
    article = requester.get_cn_solution_detail_article(self.session, article_slug)
    return article


# CN Request Interview Company Tags Tasks
@shared_task(bind=True, base=LeetcodeCNSessionBaseTask)
def get_cn_interview_hotcards_task(self) -> dict:
    hotcards = requester.get_cn_interview_hotcards(self.session)
    return hotcards


@shared_task(bind=True, base=LeetcodeCNSessionBaseTask)
def get_cn_interview_hotsearchcards_task(self) -> dict:
    hotsearchcards = requester.get_cn_interview_hotsearchcards(self.session)
    return hotsearchcards


@shared_task(bind=True, base=LeetcodeCNSessionBaseTask)
def get_cn_interview_company_tags_task(self, company_slug: str) -> dict:
    company_tags = requester.get_cn_interview_company_tags(self.session, company_slug)
    return company_tags


# Mongo Update or Insert Tasks
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


# Mongo Update ProblemStats Tags/Favorites Tasks
@shared_task
def mongo_update_favorites_all_task(favorites, cn=False, collection_name="favorites"):
    if cn:
        mongo_task = leetcodecn_update_or_insert_mongo_task
    else:
        mongo_task = leetcode_update_or_insert_mongo_task

    for favorite in favorites:
        if not requester.valid_data(favorite, "favorites"):
            logger.warning("Invalid favorite data: %s" % favorite)
            continue

        q = {"id": favorite["id"]}
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
        if not requester.valid_data(tag, "topicTags"):
            logger.warning("Invalid tag data: %s" % tag)
            continue

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
            "progress": stat_item["progress"],
            "ac_rate": stat["total_acs"] / stat["total_submitted"],
            **stat,
        }

        # Only update if frequency avaiable(Premium only)
        frequency = stat_item["frequency"]
        if frequency:
            stat_data.update(frequency=frequency)

        mongo_task.delay(collection_name=collection_name, q=q, **stat_data)


# Mongo Update Problems All Tasks
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
    if not requester.valid_data(problem, "problemContent"):
        # Premium only problems
        logger.warning(
            "Invalid problem data: %s.%s PaidOnly: %s"
            % (
                problem.get("questionFrontendId", None),
                problem.get("titleSlug", None),
                problem.get("isPaidOnly", False),
            )
        )
        return

    q = {"questionId": problem["questionId"]}
    mongo_task.delay(collection_name=collection_name, q=q, **problem)


def problems_all_workflow(get_problem_task, title_slug, stat_item, cn, collection_name):
    flow = get_problem_task.s(title_slug) | mongo_update_problem_task.s(
        stat=stat_item, cn=cn, collection_name=collection_name
    )
    return flow


@shared_task
def mongo_update_problems_all_task(stats, cn=False, collection_name="problems"):
    if cn:
        get_problem_task = get_cn_problem_by_title_slug_task
    else:
        get_problem_task = get_problem_by_title_slug_task

    problem_stats_pairs = stats.get("stat_status_pairs", [])
    for stat_item in problem_stats_pairs:
        title_slug = stat_item["stat"]["question__title_slug"]
        problems_all_workflow(
            get_problem_task, title_slug, stat_item, cn, collection_name
        ).delay()


# Mongo CN Solution Tags Tasks
@shared_task
def mongo_update_cn_problem_solution_tag_task(
    tags, stat, collection_name="solution_tags"
):
    tags_data = tags.get("data", {})
    question_id = stat["stat"]["question_id"]
    slug = stat["stat"]["question__title_slug"]
    frontend_question_id = stat["stat"]["frontend_question_id"]
    tags_data.update(
        {
            "question_id": question_id,
            "update_time": datetime.datetime.now(),
            "frontend_question_id": frontend_question_id,
            "slug": slug,
        }
    )
    q = {"question_id": tags_data["question_id"]}

    if not requester.valid_data(tags_data, "allTags"):
        # Premium only problems
        logger.warning("Invalid solution tag data: %s" % tags_data)
        return

    leetcodecn_update_or_insert_mongo_task.delay(
        collection_name=collection_name, q=q, **tags_data
    )


def solution_tags_workflow(title_slug, stat_item, collection_name):
    flow = get_cn_solution_tags_task.s(
        title_slug
    ) | mongo_update_cn_problem_solution_tag_task.s(
        stat=stat_item, collection_name=collection_name
    )
    return flow


@shared_task
def mongo_update_cn_solution_tags_task(stats, collection_name="solution_tags"):
    problem_stats_pairs = stats.get("stat_status_pairs", [])
    for stat_item in problem_stats_pairs:
        # Easily misleading stat and stat["stat"]
        title_slug = stat_item["stat"]["question__title_slug"]
        solution_tags_workflow(title_slug, stat_item, collection_name).delay()


# Mongo CN Solution Articles Tasks
@shared_task
def mongo_update_cn_article_detail_task(
    article, total_data, solution_collection="solutions"
):
    solution_article_data = article.get("data", {}).get("solutionArticle", {})
    solution_article_data.update(total_data)
    q = {
        "question_id": solution_article_data["question_id"],
        "uuid": solution_article_data["uuid"],
    }

    if not requester.valid_data(solution_article_data, "solutionArticleContent"):
        logger.warning("Invalid article data: %s" % solution_article_data)
        return

    leetcodecn_update_or_insert_mongo_task.delay(
        collection_name=solution_collection, q=q, **solution_article_data
    )


def solution_detail_workflow(article_title_slug, total_data, solution_collection):
    flow = get_cn_solution_detail_article_task.s(
        article_title_slug
    ) | mongo_update_cn_article_detail_task.s(
        total_data=total_data, solution_collection=solution_collection
    )
    return flow


@shared_task
def mongo_update_cn_solution_articles_task(
    articles,
    stat,
    solution_collection="solutions",
    totalnum_collection="solutions_total_history",
):
    r""" Problem solution articles `totalNum` data"""

    solution_articles_data = articles.get("data", {}).get(
        "questionSolutionArticles", {}
    )
    total_num = solution_articles_data.get("totalNum", 0)
    question_id = stat["stat"]["question_id"]
    frontend_id = stat["stat"]["frontend_question_id"]
    question_slug = stat["stat"]["question__title_slug"]
    question_title = stat["stat"]["question__title"]
    total_data = {
        "update_time": datetime.datetime.now(),
        "totalNum": total_num,
        "frontend_question_id": frontend_id,
        "question_id": question_id,
        "question_slug": question_slug,
        "question_title": question_title,
        "question_paid_only": stat["paid_only"],
    }
    leetcodecn_update_or_insert_mongo_task.delay(
        collection_name=totalnum_collection, q=None, **total_data
    )

    article_list = solution_articles_data.get("edges", [])
    for article in article_list:
        article_node = article.get("node", {})
        # Easily misleading stat and stat["stat"]
        article_title_slug = article_node["slug"]
        solution_detail_workflow(
            article_title_slug, total_data, solution_collection
        ).delay()


def solution_list_workflow(
    title_slug, limit, stat_item, solution_collection, totalnum_collection
):
    r"""If you want to display the progress of every problem's solution
    You may make this workflow synced...
    By: `flow().get()`
    """
    flow = get_cn_solution_list_task.s(
        title_slug, limit=limit
    ) | mongo_update_cn_solution_articles_task.s(
        stat=stat_item,
        solution_collection=solution_collection,
        totalnum_collection=totalnum_collection,
    )
    return flow


@shared_task
def mongo_update_cn_solutions_all_task(
    stats,
    limit=10,
    solution_collection="solutions",
    totalnum_collection="solutions_total_history",
):
    """CN Solution Articles All Update
    """
    problem_stats_pairs = stats.get("stat_status_pairs", [])
    for stat_item in problem_stats_pairs:
        # Easily misleading stat and stat["stat"]
        title_slug = stat_item["stat"]["question__title_slug"]
        solution_list_workflow(
            title_slug, limit, stat_item, solution_collection, totalnum_collection
        ).delay()


@shared_task
def extract_company_slugs(cards):
    slugs = []
    for card in cards:
        data_list = card.get("data", {}).get("interviewHotCards", {}) or card.get(
            "data", {}
        ).get("interviewHotSearchHistory", {})
        for item in data_list:
            company = item.get("company", {}) or {}
            slug = company.get("slug", None)
            if slug and slug not in slugs:
                slugs.append(slug)
    return slugs


@shared_task
def get_cn_company_slugs_all() -> list:
    hotcards = get_cn_interview_hotcards_task.s()
    hotsearchs = get_cn_interview_hotsearchcards_task.s()
    flow = chord(hotcards, hotsearchs)(extract_company_slugs.s())
    return flow


@shared_task
def mongo_update_cn_interview_company_tag(
    company_tag, company_slug, company_tags_collection="company_tags",
):
    data = company_tag.get("data", {})
    # if valid
    if not requester.valid_data(data, "companyTag"):
        logger.warning("Invalid company tags data for %s: %s" % (company_slug, data))
        return

    data.update({"company_slug": company_slug})
    q = {"company_slug": company_slug}
    leetcodecn_update_or_insert_mongo_task(
        collection_name=company_tags_collection, q=q, **data
    )


@shared_task
def mongo_update_cn_interview_company_tags_all(
    company_slugs, company_tags_collection="company_tags",
):
    for slug in company_slugs:
        flow = (
            get_cn_interview_company_tags_task.s(company_slug=slug)
            | mongo_update_cn_interview_company_tag.s(
                company_slug=slug, company_tags_collection=company_tags_collection
            )
        )()
