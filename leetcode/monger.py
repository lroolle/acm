""" A stupid async data preservation process to mongoDB"""

import logging

import pymongo
from celery import chord
from leetcode import tasks
from tqdm import tqdm

logger = logging.getLogger(__name__)


def init_client():
    logger.debug("Init pymongo client...")
    client = pymongo.MongoClient("localhost", 27017)
    return client


def tqdm_flow(flow, desc=""):
    """ tqdm result progress bar for workflow created by celery chain/group"""
    for result in tqdm(flow.children, total=len(flow.children), desc=desc):
        try:
            result.get()
        except Exception as e:
            logger.error(e)
            logger.debug(result.task_id)


def update_favorites_all():
    # Leetcode.com
    logger.debug("Starting leetcode update_favorites_all_task")
    flow = (
        tasks.get_problem_favorites_all_task.s()
        | tasks.mongo_update_favorites_all_task.s(cn=False)
    )()
    flow.get()
    tqdm_flow(flow, desc="   Favorites")

    # Leetcode-cn.com
    logger.debug("Starting leetcode-cn update_favorites_all_task")
    flow_cn = (
        tasks.get_cn_problem_favorites_all_task.s()
        | tasks.mongo_update_favorites_all_task.s(cn=True)
    )()
    flow_cn.get()
    tqdm_flow(flow_cn, desc="CN Favorites")


def update_tags_all():
    # Leetcode.com
    logger.debug("Starting leetcode update_tags_all_task")
    flow = (
        tasks.get_problem_tags_all_task.s()
        | tasks.mongo_update_tags_all_task.s(cn=False)
    )()
    flow.get()
    tqdm_flow(flow, desc="   Tags")

    # Leetcode-cn.com
    logger.debug("Starting leetcode-cn update_tags_all_task")
    flow_cn = (
        tasks.get_cn_problem_tags_all_task.s()
        | tasks.mongo_update_tags_all_task.s(cn=True)
    )()
    flow_cn.get()
    tqdm_flow(flow_cn, desc="CN Tags")


def update_problem_stats_all():
    # Leetcode.com
    logger.debug("Starting leetcode update_problem_stats_all_task")
    flow = (
        tasks.get_problem_stats_all_task.s()
        | tasks.mongo_update_problem_stats_all_task.s(cn=False)
    )()
    flow.get()
    tqdm_flow(flow, desc="   Stats")

    # Leetcode-cn.com
    logger.debug("Starting leetcode-cn update_problem_stats_all_task")
    flow_cn = (
        tasks.get_cn_problem_stats_all_task.s()
        | tasks.mongo_update_problem_stats_all_task.s(cn=True)
    )()
    flow_cn.get()
    tqdm_flow(flow_cn, desc="CN Stats")


def update_problems_all():
    # Leetcode.com
    logger.debug("Starting leetcode update_problem_all_task")
    flow = (
        tasks.get_problem_stats_all_task.s()
        | tasks.mongo_update_problems_all_task.s(cn=False)
    )()
    flow.get()
    # TODO: Can be a Thread...
    # BUG: Protocol error, redis connection share thread?
    # thread = threading.Thread(target=tqdm_flow, args=(flow, "Leetcode"))
    # thread.start()
    tqdm_flow(flow, "   Problems")

    # Leetcode-cn.com
    logger.debug("Starting leetcode-cn update_problem_all_task")
    flow_cn = (
        tasks.get_cn_problem_stats_all_task.s()
        | tasks.mongo_update_problems_all_task.s(cn=True)
    )()
    flow_cn.get()
    tqdm_flow(flow_cn, desc="CN Problems")


def update_cn_solution_tags_all():
    # Leetcode-cn.com
    logger.debug("Starting leetcode-cn update_solution_tags_all_task")
    flow_cn = (
        tasks.get_cn_problem_stats_all_task.s()
        | tasks.mongo_update_problems_all_task.s(cn=True)
    )()
    flow_cn.get()
    tqdm_flow(flow_cn, desc="CN SolutionTags")


def update_cn_solution_articles_all(limit=10):
    # Leetcode-cn.com
    logger.debug("Starting leetcode-cn update_solution_articles_task")
    flow_cn = (
        tasks.get_cn_problem_stats_all_task.s()
        | tasks.mongo_update_cn_solutions_all_task.s(limit=limit)
    )()
    # This may just displays get_solution_list process of each problem
    # But no get solution detail process due to async works...
    flow_cn.get()
    logger.warning(
        "This process only displays solution list of each problem, "
        "Which means there are still article detail tasks running background..."
    )
    tqdm_flow(flow_cn, desc="CN Solutions")


def update_cn_company_tags_all():
    # Leetcode-cn.com
    logger.debug("Starting leetcode-cn update_company_tags_task")
    hotcards = tasks.get_cn_interview_hotcards_task.s()
    hotsearchs = tasks.get_cn_interview_hotsearchcards_task.s()
    flow_cn = chord(hotcards, hotsearchs)(
        tasks.extract_company_slugs.s()
        | tasks.mongo_update_cn_interview_company_tags_all.s()
    )
    flow_cn.get()
    tqdm_flow(flow_cn, desc="CN CompanyTags")


def update_all():
    update_favorites_all()
    update_tags_all()
    update_problem_stats_all()
    update_problems_all()
    update_cn_company_tags_all()
    update_cn_solution_tags_all()
    update_cn_solution_articles_all()
