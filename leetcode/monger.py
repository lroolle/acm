""" A stupid data preservation to mongoDB"""

import datetime
import logging
import random
import time

import pymongo
import requests
from tqdm import tqdm

from leetcode import requester as fetcher
from leetcode import tasks

logger = logging.getLogger(__name__)


def init_client():
    logger.debug("Init pymongo client...")
    client = pymongo.MongoClient("localhost", 27017)
    return client


def update_favorites_all():
    # Leetcode.com
    logger.debug("Starting leetcode update_favorites_all_task")
    flow = (
        tasks.get_problem_favorites_all_task.s()
        | tasks.mongo_update_favorites_all_task.s(cn=False)
    )()
    flow.get()
    for result in tqdm(flow.children, total=len(flow.children)):
        result.get()

    # Leetcode-cn.com
    logger.debug("Starting leetcode-cn update_favorites_all_task")
    flow = (
        tasks.get_cn_problem_favorites_all_task.s()
        | tasks.mongo_update_favorites_all_task.s(cn=True)
    )()
    flow.get()
    for result in tqdm(flow.children, total=len(flow.children)):
        result.get()


def update_tags_all():
    # Leetcode.com
    logger.debug("Starting leetcode update_tags_all_task")
    flow = (
        tasks.get_problem_tags_all_task.s()
        | tasks.mongo_update_tags_all_task.s(cn=False)
    )()
    flow.get()
    for result in tqdm(flow.children, total=len(flow.children)):
        result.get()

    # Leetcode-cn.com
    logger.debug("Starting leetcode-cn update_tags_all_task")
    flow = (
        tasks.get_cn_problem_tags_all_task.s()
        | tasks.mongo_update_tags_all_task.s(cn=True)
    )()
    flow.get()
    for result in tqdm(flow.children, total=len(flow.children)):
        result.get()


def update_problem_stats_all():
    # Leetcode.com
    logger.debug("Starting leetcode update_problem_stats_all_task")
    flow = (
        tasks.get_problem_stats_all_task.s()
        | tasks.mongo_update_problem_stats_all_task.s(cn=False)
    )()
    flow.get()
    for result in tqdm(flow.children, total=len(flow.children)):
        result.get()

    # Leetcode-cn.com
    logger.debug("Starting leetcode-cn update_problem_stats_all_task")
    flow_cn = (
        tasks.get_cn_problem_stats_all_task.s()
        | tasks.mongo_update_problem_stats_all_task.s(cn=True)
    )()
    flow_cn.get()
    for result in tqdm(flow_cn.children, total=len(flow_cn.children)):
        result.get()


def update_problems_all():
    # Leetcode.com
    logger.debug("Starting leetcode update_problem_all_task")
    flow = (
        tasks.get_problem_stats_all_task.s()
        | tasks.mongo_update_problems_all_task.s(cn=False)
    )()
    flow.get()
    for result in tqdm(flow.children, total=len(flow.children)):
        result.get()

    # Leetcode-cn.com
    logger.debug("Starting leetcode-cn update_problem_all_task")
    flow = (
        tasks.get_problem_stats_all_task.s()
        | tasks.mongo_update_problems_all_task.s(cn=False)
    )()
    flow.get()
    for result in tqdm(flow.children, total=len(flow.children)):
        result.get()


def update_or_create_problems(db, session, f):
    collection = db.problems
    for stat in db.problem_stats.find():
        question_id = stat["question_id"]
        title_slug = stat["question__title_slug"]
        # Should be a task
        problem = f(session, title_slug)
        problem.update(
            {
                "question_id": question_id,
                "update_time": datetime.datetime.now(),
                "stat": stat,
            }
        )
        # NOTE: Type of problem["questioId"] is string
        q = {"questionId": problem["questionId"]}
        if collection.find_one(q):
            collection.update_one(q, {"$set": problem})
            logger.debug(
                "Uupdated: %s.%s"
                % (problem["questionFrontendId"], problem["titleSlug"])
            )
            continue
        logger.debug(
            "Inserted: %s.%s" % (problem["questionFrontendId"], problem["titleSlug"])
        )
        collection.insert_one(problem)


def get_problems(session: requests.Session, client: pymongo.MongoClient):
    # Leetcode.com
    # logger.debug("Fetching leetcode    problems all.")
    # db = client.leetcode
    # update_or_create_problems(
    #     db=db, session=session, f=fetcher.get_problem_by_title_slug
    # )
    # Leetcode-cn.com
    logger.debug("Fetching leetcode-cn problems all.")
    db_cn = client.leetcode_cn
    update_or_create_problems(
        db=db_cn, session=session, f=fetcher.get_cn_problem_by_title_slug
    )


def get_cn_solution_tags(session: requests.Session, client: pymongo.MongoClient):
    collection = client.leetcode_cn.solution_tags

    for stat in client.leetcode_cn.problem_stats.find():
        question_id = stat["question_id"]
        frontend_question_id = stat["frontend_question_id"]
        slug = stat["question__title_slug"]

        tags = fetcher.get_cn_solution_tags_list(session, slug)
        data = tags.get("data")
        if not data:
            continue

        solution_tags = data.get("solutionTags")
        if not solution_tags:
            continue

        solution_tags = {
            "update_time": datetime.datetime.now(),
            "frontend_question_id": frontend_question_id,
            "question_id": question_id,
            "slug": slug,
            **solution_tags,
        }

        q = {"question_id": question_id}
        exist_one = collection.find_one(q)
        if exist_one:
            logger.debug("SolutonTags uupdated: %s.%s" % (frontend_question_id, slug))
            collection.update_one(q, {"$set": solution_tags})
            continue

        logger.debug("SolutonTags Inserted: %s.%s" % (frontend_question_id, slug))
        collection.insert_one(solution_tags)


def get_cn_solutions(session: requests.Session, client: pymongo.MongoClient):
    collection = client.leetcode_cn.solutions
    problem_stats = client.leetcode_cn.problem_stats.find()
    problem_stats_count = client.leetcode_cn.problem_stats.count()

    for i, stat in enumerate(problem_stats):
        question_id = stat["question_id"]
        frontend_id = stat["frontend_question_id"]
        question_slug = stat["question__title_slug"]
        question_title = stat["question__title"]
        logger.debug(
            f"==> [{i+1}/{problem_stats_count}:{100 * (i+1)/problem_stats_count:02.0f}%] {frontend_id}.{question_title}: {question_slug}."
        )
        solution_list = fetcher.get_cn_solution_list(session, question_slug)
        solution_articles = solution_list.get("data", {}).get(
            "questionSolutionArticles", {}
        )

        total_num = solution_articles.get("totalNum")
        if (
            not solution_articles.get("edges")
            or solution_articles.get("totalNum", 0) < 1
        ):
            no_data = {
                "update_time": datetime.datetime.now(),
                "frontend_question_id": frontend_id,
                "question_id": question_id,
                "question_slug": question_slug,
                "question_title": question_title,
                "question_paid_only": stat["paid_only"],
                "total_num": total_num,
            }
            collection.insert_one(no_data)
            logger.debug(
                f"xx> {frontend_id}.{question_title}: Found 0 solution_article!"
            )
            continue

        for i, solution_article in enumerate(solution_articles["edges"]):
            solution_article_node = solution_article.get("node", {})
            if not solution_article_node:
                continue

            solution_article_data = {
                "update_time": datetime.datetime.now(),
                "frontend_question_id": frontend_id,
                "question_id": question_id,
                "question_slug": question_slug,
                "question_title": question_title,
                "question_paid_only": stat["paid_only"],
                "total_num": total_num,
                **solution_article_node,
            }
            article_slug = solution_article_node["slug"]
            article_detail = fetcher.get_cn_solution_detail_article(
                session, article_slug
            )
            solution_article_data.update(
                article_detail.get("data", {}).get("solutionArticle", {})
            )

            q = {"question_id": question_id, "uuid": solution_article_node["uuid"]}
            exist_one = collection.find_one(q)
            if exist_one:
                collection.update_one(q, {"$set": solution_article_data})
                logger.debug(
                    "[%02d] Uupdated: %s by %s"
                    % (
                        i + 1,
                        solution_article_data["title"],
                        solution_article_data["author"]["username"],
                    )
                )
                continue
            logger.debug(
                "[%02d] Inserted: %s by %s"
                % (
                    i + 1,
                    solution_article_data["title"],
                    solution_article_data["author"]["username"],
                )
            )
            collection.insert_one(solution_article_data)


def update_all(client: pymongo.MongoClient, session: requests.Session):
    get_favorites(session, client)
    get_tags(session, client)
    get_problem_stats(session, client)
    get_problems(session, client)
    get_cn_solution_tags(session, client)
    get_cn_solutions(session, client)
