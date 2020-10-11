import http
import itertools
import json
import logging
from functools import wraps
from typing import List

import browser_cookie3
import requests
from requests.exceptions import RequestException
from requests.packages import urllib3

from leetcode import config

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
)

DOMAIN = "leetcode.com"
DOMAIN_CN = "leetcode-cn.com"
GRAPHQL = f"https://{DOMAIN}/graphql"
GRAPHQL_CN = f"https://{DOMAIN_CN}/graphql"


class RequestException(RequestException, urllib3.exceptions.HTTPError):
    """ A request exception"""


class BadRequest(RequestException):
    """ Unexpected response due to a BAD request Eww..."""


class NotAuthenticated(RequestException):
    """ Authetication required to request."""


def login_required(domain):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            session = list(
                filter(
                    lambda x: isinstance(x, requests.Session),
                    itertools.chain(args, kwargs.values()),
                )
            )
            if not session:
                raise NotAuthenticated("Session not found")

            logged_in = session[0].cookies.get("LEETCODE_SESSION", domain=domain)
            if not bool(logged_in):
                raise NotAuthenticated(
                    "Sign in to %s is required to %s." % (domain, f.__name__)
                )
            return f(*args, **kwargs)

        return wrapper

    return decorator


def get_cookies_csrftoken(session: requests.Session, domain: str) -> str:
    """
    The token in leetcode.com domain named: <csrftoken for leetcode.com>
    The token in leetcode-cn.com domain named: <csrftoken for .leetcode-cn.com token>
    """
    csrftokens = filter(
        lambda x: x.name == "csrftoken" and x.domain.endswith(domain), session.cookies,
    )
    x_csrftoken = ""
    for token in csrftokens:
        x_csrftoken = token.value
    return x_csrftoken


def get_problem_by_title_slug(session: requests.Session, title_slug: str) -> dict:
    """ Return leetcode.com data.question data through graphql api.
    Errors raised when data not as expected, or HttpRequestTimeout or ConnectionError or ...
    You may try catch to get in your module.
    """
    payload = {
        "operationName": "questionData",
        "variables": {"titleSlug": title_slug},
        "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      paidOnly\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    enableDebugger\n    envInfo\n    libraryUrl\n    adminUrl\n    __typename\n  }\n}\n",
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Referer": f"https://{DOMAIN}/problems/{title_slug}",
        "X-CSRFToken": get_cookies_csrftoken(session, DOMAIN),
    }
    resp = session.post(GRAPHQL, data=json.dumps(payload), headers=headers, timeout=20)
    resp_json = resp.json()
    if resp_json.get("errors", ""):
        raise BadRequest(
            "Error get problem by title slug: %s" % str(resp_json["errors"])
        )

    return resp_json["data"]["question"]


def get_cn_problem_by_title_slug(session: requests.Session, title_slug: str) -> dict:
    """ Return leetcode-cn.com data.question data through graphql api.
    Errors raised when data not as expected, or HttpRequestTimeout or ConnectionError or ...
    You may try catch to get in your module.
    """
    payload = {
        "operationName": "questionData",
        "variables": {"titleSlug": title_slug},
        "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    envInfo\n    book {\n      id\n      bookName\n      pressName\n      source\n      shortDescription\n      fullDescription\n      bookImgUrl\n      pressImgUrl\n      productUrl\n      __typename\n    }\n    isSubscribed\n    isDailyQuestion\n    dailyRecordStatus\n    editorType\n    ugcQuestionId\n    style\n    __typename\n  }\n}\n",
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Referer": f"https://{DOMAIN_CN}/problems/{title_slug}/",
        "X-CSRFToken": get_cookies_csrftoken(session, DOMAIN_CN),
    }
    resp = session.post(GRAPHQL_CN, data=json.dumps(payload), headers=headers)
    resp_json = resp.json()
    if resp_json.get("errors", ""):
        raise BadRequest(
            "Error get cn problem by title slug: %s" % str(resp_json["errors"])
        )

    return resp_json["data"]["question"]


def get_problem_tags_all(session: requests.Session) -> dict:
    url = f"https://{DOMAIN}/problems/api/tags/"
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
        "Referer": f"https://{DOMAIN}/problemset/all/",
    }
    resp = session.get(url, headers=headers)
    return resp.json()


def get_cn_problem_tags_all(session: requests.Session) -> dict:
    url = f"https://{DOMAIN_CN}/problems/api/tags/"
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
        "Referer": f"https://{DOMAIN_CN}/problemset/all/",
    }
    resp = session.get(url, headers=headers)
    return resp.json()


def get_problem_favorites_all(session: requests.Session) -> dict:
    url = f"https://{DOMAIN}/problems/api/favorites/"
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
        "Referer": f"https://{DOMAIN}/problemset/all/",
    }
    resp = session.get(url, headers=headers)
    return resp.json()


def get_cn_problem_favorites_all(session: requests.Session) -> dict:
    url = f"https://{DOMAIN_CN}/problems/api/favorites/"
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
        "Referer": f"https://{DOMAIN_CN}/problemset/all/",
    }
    resp = session.get(url, headers=headers)
    return resp.json()


def get_cn_problem_of_today(session: requests.Session) -> dict:
    payload = {
        "operationName": "questionOfToday",
        "variables": {},
        "query": "query questionOfToday {\n  todayRecord {\n    question {\n      questionFrontendId\n      questionTitleSlug\n      __typename\n    }\n    lastSubmission {\n      id\n      __typename\n    }\n    date\n    userStatus\n    __typename\n  }\n}\n",
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Referer": f"https://{DOMAIN_CN}/problemset/all/",
        "X-CSRFToken": get_cookies_csrftoken(session, DOMAIN_CN),
    }
    resp = session.post(GRAPHQL_CN, data=json.dumps(payload), headers=headers)
    return resp.json()


def get_cn_solution_tags_list(session: requests.Session, slug: str) -> dict:
    payload = {
        "operationName": "solutionTags",
        "variables": {"questionSlug": slug},
        "query": "query solutionTags($questionSlug: String!) {\n  solutionTags(questionSlug: $questionSlug) {\n    allTags {\n      name\n      nameTranslated\n      slug\n      __typename\n    }\n    languageTags {\n      name\n      nameTranslated\n      slug\n      __typename\n    }\n    otherTags {\n      name\n      nameTranslated\n      slug\n      __typename\n    }\n    __typename\n  }\n}\n",
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Referer": f"https://{DOMAIN_CN}/problems/{slug}/solution/",
        "X-CSRFToken": get_cookies_csrftoken(session, DOMAIN_CN),
    }
    resp = session.post(GRAPHQL_CN, data=json.dumps(payload), headers=headers)
    return resp.json()


def get_cn_solution_list(
    session: requests.Session,
    slug: str,
    limit: int = 10,
    order_by: str = "DEFAULT",
    tag_slugs: List[str] = list(),
    q: str = "",
) -> dict:
    payload = {
        "operationName": "questionSolutionArticles",
        "variables": {
            "questionSlug": slug,
            "first": limit,
            "skip": 0,
            "orderBy": order_by,
            "tagSlugs": tag_slugs,
            "userInput": q,
        },
        "query": "query questionSolutionArticles($questionSlug: String!, $skip: Int, $first: Int, $orderBy: SolutionArticleOrderBy, $userInput: String, $tagSlugs: [String!]) {\n  questionSolutionArticles(questionSlug: $questionSlug, skip: $skip, first: $first, orderBy: $orderBy, userInput: $userInput, tagSlugs: $tagSlugs) {\n    totalNum\n    edges {\n      node {\n        ...solutionArticle\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment solutionArticle on SolutionArticleNode {\n  uuid\n  title\n  slug\n  sunk\n  chargeType\n  status\n  identifier\n  canEdit\n  reactionType\n  reactionsV2 {\n    count\n    reactionType\n    __typename\n  }\n  tags {\n    name\n    nameTranslated\n    slug\n    __typename\n  }\n  createdAt\n  thumbnail\n  author {\n    username\n    profile {\n      userAvatar\n      userSlug\n      realName\n      __typename\n    }\n    __typename\n  }\n  summary\n  topic {\n    id\n    commentCount\n    viewCount\n    __typename\n  }\n  byLeetcode\n  isMyFavorite\n  isMostPopular\n  isEditorsPick\n  hitCount\n  videosInfo {\n    videoId\n    coverUrl\n    duration\n    __typename\n  }\n  __typename\n}\n",
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Referer": f"https://{DOMAIN_CN}/problems/{slug}/solution/",
        "X-CSRFToken": get_cookies_csrftoken(session, DOMAIN_CN),
    }
    resp = session.post(GRAPHQL_CN, data=json.dumps(payload), headers=headers)
    return resp.json()


def get_cn_solution_detail_article(session: requests.Session, slug: str) -> dict:
    payload = {
        "operationName": "solutionDetailArticle",
        "variables": {"slug": slug, "orderBy": "DEFAULT"},
        "query": "query solutionDetailArticle($slug: String!, $orderBy: SolutionArticleOrderBy!) {\n  solutionArticle(slug: $slug, orderBy: $orderBy) {\n    ...solutionArticle\n    content\n    question {\n      questionTitleSlug\n      __typename\n    }\n    position\n    next {\n      slug\n      title\n      __typename\n    }\n    prev {\n      slug\n      title\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment solutionArticle on SolutionArticleNode {\n  uuid\n  title\n  slug\n  sunk\n  chargeType\n  status\n  identifier\n  canEdit\n  reactionType\n  reactionsV2 {\n    count\n    reactionType\n    __typename\n  }\n  tags {\n    name\n    nameTranslated\n    slug\n    __typename\n  }\n  createdAt\n  thumbnail\n  author {\n    username\n    profile {\n      userAvatar\n      userSlug\n      realName\n      __typename\n    }\n    __typename\n  }\n  summary\n  topic {\n    id\n    commentCount\n    viewCount\n    __typename\n  }\n  byLeetcode\n  isMyFavorite\n  isMostPopular\n  isEditorsPick\n  hitCount\n  videosInfo {\n    videoId\n    coverUrl\n    duration\n    __typename\n  }\n  __typename\n}\n",
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Referer": f"https://{DOMAIN_CN}/problems/{slug}/solution/",
        "X-CSRFToken": get_cookies_csrftoken(session, DOMAIN_CN),
    }
    resp = session.post(GRAPHQL_CN, data=json.dumps(payload), headers=headers)
    return resp.json()


def get_cn_interview_hotcards(session: requests.Session) -> dict:
    """ 企业题库(Vip Maybe Required)"""
    payload = {
        "operationName": "interviewHotCards",
        "variables": {},
        "query": "query interviewHotCards {\n  interviewHotCards {\n    id\n    acRate\n    order\n    isFavorite\n    isPremiumOnly\n    numParticipants\n    numQuestionsAced\n    numQuestions\n    privilegeExpiresAt\n    company {\n      name\n      slug\n      imgUrl\n      __typename\n    }\n    jobsCompany {\n      name\n      jobPostingNum\n      isVerified\n      __typename\n    }\n    __typename\n  }\n}\n",
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Referer": f"https://{DOMAIN_CN}/problems/interview/",
        "X-CSRFToken": get_cookies_csrftoken(session, DOMAIN_CN),
    }
    resp = session.post(GRAPHQL_CN, data=json.dumps(payload), headers=headers)
    return resp.json()


def get_cn_interview_hotsearchcards(session: requests.Session) -> dict:
    """ 企业题库-热搜企业(Vip Maybe Required)"""
    payload = {
        "operationName": "interviewHotSearchCards",
        "variables": {"num": 100},
        "query": "query interviewHotSearchCards($num: Int) {\n  interviewHotSearchHistory(num: $num) {\n    company {\n      name\n      slug\n      imgUrl\n      __typename\n    }\n    __typename\n  }\n}\n",
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Referer": f"https://{DOMAIN_CN}/problems/interview/",
        "X-CSRFToken": get_cookies_csrftoken(session, DOMAIN_CN),
    }
    resp = session.post(GRAPHQL_CN, data=json.dumps(payload), headers=headers)
    return resp.json()


def get_cn_interview_company_tags(session: requests.Session, slug: str) -> dict:
    payload = {
        "operationName": "companyTag",
        "variables": {"slug": slug},
        "query": "query companyTag($slug: String!) {\n  interviewCard(companySlug: $slug) {\n    id\n    isFavorite\n    isPremiumOnly\n    privilegeExpiresAt\n    jobsCompany {\n      name\n      jobPostingNum\n      isVerified\n      description\n      logo\n      logoPath\n      postingTypeCounts {\n        count\n        postingType\n        __typename\n      }\n      industryDisplay\n      scaleDisplay\n      financingStageDisplay\n      website\n      legalName\n      __typename\n    }\n    __typename\n  }\n  interviewCompanyOptions(query: $slug) {\n    id\n    __typename\n  }\n  companyTag(slug: $slug) {\n    name\n    id\n    imgUrl\n    translatedName\n    frequencies\n    questions {\n      title\n      translatedTitle\n      titleSlug\n      questionId\n      stats\n      status\n      questionFrontendId\n      difficulty\n      frequencyTimePeriod\n      topicTags {\n        id\n        name\n        slug\n        translatedName\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  jobsCompany(companySlug: $slug) {\n    name\n    legalName\n    logo\n    description\n    website\n    industryDisplay\n    scaleDisplay\n    financingStageDisplay\n    isVerified\n    __typename\n  }\n}\n",
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Referer": f"https://{DOMAIN_CN}/problems/interview/",
        "X-CSRFToken": get_cookies_csrftoken(session, DOMAIN_CN),
    }
    resp = session.post(GRAPHQL_CN, data=json.dumps(payload), headers=headers)
    return resp.json()


@login_required(f".{DOMAIN}")
def submit_problem(
    session: requests.Session, slug: str, frontend_id: str, lang: str, code: str
) -> int:
    url = f"https://{DOMAIN}/problems/{slug}/submit/"
    payload = {
        "question_id": frontend_id,
        "lang": lang,
        "typed_code": code,
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": f"https://{DOMAIN}/",
        "Referer": f"https://{DOMAIN}/problems/{slug}/submissions/",
        "X-CSRFToken": get_cookies_csrftoken(session, DOMAIN),
    }
    resp = session.post(url, data=json.dumps(payload), headers=headers)
    submission_id = resp.json().get("submission_id", None)
    if not submission_id:
        raise BadRequest("Error submit %s" % resp.text)

    return submission_id


@login_required(f".{DOMAIN_CN}")
def submit_cn_problem(
    session: requests.Session, slug: str, frontend_id: str, lang: str, code: str
) -> int:
    url = f"https://{DOMAIN_CN}/problems/{slug}/submit/"
    payload = {
        "question_id": frontend_id,
        "lang": lang,
        "typed_code": code,
        "test_mode": False,
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Referer": f"https://{DOMAIN_CN}/problems/{slug}/submissions/",
        "Origin": "https://leetcode-cn.com/",
        "Content-Type": "application/json",
        "X-CSRFToken": get_cookies_csrftoken(session, DOMAIN_CN),
    }
    resp = session.post(url, data=json.dumps(payload), headers=headers,)
    submission_id = resp.json().get("submission_id", None)
    return submission_id


@login_required(f".{DOMAIN}")
def submission_check(session: requests.Session, submission_id: int) -> int:
    url = f"https://{DOMAIN}/submissions/detail/{submission_id}/check"
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
        "Connection": "keep-alive",
    }
    resp = session.get(url, headers=headers, timeout=5)
    return resp.json()


@login_required(f".{DOMAIN_CN}")
def submission_check_cn(session: requests.Session, submission_id: int) -> int:
    url = f"https://{DOMAIN_CN}/submissions/detail/{submission_id}/check"
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
        "Connection": "keep-alive",
    }
    resp = session.get(url, headers=headers, timeout=2)
    return resp.json()


@login_required(f".{DOMAIN_CN}")
def get_cn_global_data(session: requests.Session) -> dict:
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Referer": f"https://{DOMAIN_CN}/",
        "Origin": f"https://{DOMAIN_CN}/",
        "Content-Type": "application/json",
    }
    payload = {
        "operationName": "globalData",
        "variables": {},
        "query": "query globalData {\n  feature {\n    questionTranslation\n    subscription\n    signUp\n    discuss\n    mockInterview\n    contest\n    store\n    book\n    chinaProblemDiscuss\n    socialProviders\n    studentFooter\n    cnJobs\n    enableLsp\n    enableWs\n    enableDebugger\n    enableDebuggerAdmin\n    enableDarkMode\n    tasks\n    leetbook\n    enableEduDiscount\n    __typename\n  }\n  userStatus {\n    isSignedIn\n    isAdmin\n    isStaff\n    isSuperuser\n    isTranslator\n    isPremium\n    isVerified\n    isPhoneVerified\n    isWechatVerified\n    checkedInToday\n    username\n    realName\n    userSlug\n    groups\n    avatar\n    optedIn\n    requestRegion\n    region\n    socketToken\n    activeSessionId\n    permissions\n    notificationStatus {\n      lastModified\n      numUnread\n      __typename\n    }\n    completedFeatureGuides\n    useTranslation\n    accountStatus {\n      isFrozen\n      inactiveAfter\n      __typename\n    }\n    __typename\n  }\n  siteRegion\n  chinaHost\n  websocketUrl\n  userBannedInfo {\n    bannedData {\n      endAt\n      bannedType\n      __typename\n    }\n    __typename\n  }\n  commonNojPermissionTypes\n}\n",
    }
    resp = session.post(
        GRAPHQL_CN, headers=headers, data=json.dumps(payload), timeout=10
    )
    return resp.json()


def signedin_cn(session: requests.Session) -> bool:
    """ Session signed in leetcode-cn.com
        By graphql `usesrstatus`
    """
    global_data = get_cn_global_data(session)
    user_state = global_data.get("data", {}).get("userStatus", {})
    is_signed_in = user_state.get("isSignedIn", False)
    user_slug = user_state.get("userSlug", None)
    logger.info(f"User: {user_slug} SignedIn: {is_signed_in}")
    return is_signed_in


def verified_cn(session: requests.Session) -> bool:
    global_data = get_cn_global_data(session)
    user_state = global_data.get("data", {}).get("userStatus", {})
    is_verified = user_state.get("isVerified", False)
    user_slug = user_state.get("userSlug", None)
    logger.info(f"User: {user_slug} Verified: {is_verified}")
    return is_verified


def get_problem_stats_all(session: requests.Session) -> dict:
    url = f"https://{DOMAIN}/api/problems/all/"
    headers = {
        "User-Agent": USER_AGENT,
        "Referer": f"https://{DOMAIN}/problemset/all/",
        "Content-Type": "application/json",
    }
    resp = session.get(url, headers=headers)
    return resp.json()


def get_cn_problem_stats_all(session: requests.Session) -> dict:
    url = f"https://{DOMAIN_CN}/api/problems/all/"
    headers = {
        "User-Agent": USER_AGENT,
        "Referer": f"https://{DOMAIN_CN}/problemset/all/",
        "Content-Type": "application/json",
    }
    resp = session.get(url, headers=headers)
    return resp.json()


def login(session: requests.Session, username: str = "", password: str = ""):
    """ TODO: Login leetcode.com after fucking recaptcha"""
    base_url = "https://leetcode.com"
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "origin": base_url,
    }
    index_resp = session.get(base_url, headers=headers)
    cookies = index_resp.cookies
    csrftoken = list(filter(lambda x: x.name == "csrftoken", cookies))[0].value

    login_url = "https://leetcode.com/accounts/login"
    params_data = {
        "csrfmiddlewaretoken": csrftoken,
        "login": username,
        "password": password,
        "next": "/",
        "recaptcha_token": "03AGdBq24X1GY-83PM5T1IDJFZoNLWkJP7QV-2nsldeWy_6ugViiSIH2lCEh5DrfIdUqPn7F2Poq2Ilh0tbtZXnjFlAJnbhjHLD2CHol0i054zcn6wCybG951ET9-Sk4eNUvkXPIxqL6V_QNUw0EN9xUApbXUCj8GNFQ37H61lYx-3rrJpX74C602jNwlxG_mar4Ab1CNGnf40F0Rgl0tZumVJTBS8FnSTJlEisp-VCyKH7uUCp7-LiunBApTvlRNyPzEG9eBkTXeEyIoaPkEInWpbv2a0ZlZIz-tNA7wh_iE2azkv-0MgnLrXfAaZpIgJZWzCQY0orUi4L-Fg6rMIpnC4er_ShbBBQS0c-Mu22q1qQthkJ98Gy2z98QOmAqiUENmAObU09Q6o",
    }

    payload = requests_toolbelt.MultipartEncoder(params_data)
    headers.update(Referer="https://leetcode.com/accounts/login/")
    headers.update({"Content-Type": payload.content_type})
    resp = session.post(
        login_url, headers=headers, data=payload, timeout=20, allow_redirects=False
    )
    is_login = session.cookies.get("LEETCODE_SESSION") != None
    # TODO: Unverified Fucking recaptcha...
    return is_login


def get_recaptcha():
    url = "https://www.recaptcha.net/recaptcha/api2/reload?k=6LdBpsIUAAAAAKAYWjZfIpn4cJHVIk_tsmxpl7cz"
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Content-Type": "application/json; charset=utf-8",
        "origin": "https://www.recaptcha.net",
        "referer": "https://www.recaptcha.net/recaptcha/api2/anchor?ar=1&k=6LdBpsIUAAAAAKAYWjZfIpn4cJHVIk_tsmxpl7cz&co=aHR0cHM6Ly9sZWV0Y29kZS5jb206NDQz&hl=en&v=NjbyeWjjFy97MXGZ40KrXu3v&size=invisible&cb=7e9mbutglfrx",
    }
    # FUCK RECAPTCHA


def login_cn(session: requests.Session, username: str = "", password: str = "") -> bool:
    """ Session login to leetcode-cn.com by set-cookies
    """
    # Clear cookies if last login
    cookies_list_domains = session.cookies.list_domains()
    if DOMAIN_CN in cookies_list_domains:
        session.cookies.clear(domain=DOMAIN_CN)
    if f".{DOMAIN_CN}" in cookies_list_domains:
        session.cookies.clear(domain=f".{DOMAIN_CN}")

    login_url = f"https://{DOMAIN_CN}/accounts/login/"
    headers = {
        "User-Agent": USER_AGENT,
        "Connection": "keep-alive",
        "Referer": login_url,
        "origin": f"https://{DOMAIN_CN}",
    }
    payload = {"login": username, "password": password}
    session.post(login_url, headers=headers, data=payload, allow_redirects=False)
    print(session.cookies)
    return bool(session.cookies.get("LEETCODE_SESSION", domain=f".{DOMAIN_CN}"))


def cookiejar_from_string(
    cookies_raw: str, domain: str = "leetcode.com", path="/", max_age: int = 14
) -> requests.cookies.RequestsCookieJar:
    """ Loads a manually copy/paste plain string cookies format
        for example "cookies: a=b; c=d" to RequestsCookieJar
    """
    cookies_raw = cookies_raw.strip().strip("cookie: ").strip("Cookie: ")
    sc = http.cookies.SimpleCookie()
    sc.load(cookies_raw)
    rcj = requests.cookies.RequestsCookieJar()
    for name, c in sc.items():
        c["domain"] = domain
        c["path"] = path
        c["max-age"] = max_age
        rcj.set(name, c)

    return rcj


def cookiejar_from_cookiestxt(filename: str) -> requests.cookies.RequestsCookieJar:
    """ Loads a Mozilla/Netscape `cookies.txt` format to RequestsCookieJar"""
    mcj = http.cookiejar.MozillaCookieJar(filename)
    mcj.load(ignore_discard=True, ignore_expires=True)
    rcj = requests.cookies.RequestsCookieJar()
    rcj.update(mcj)
    return rcj


class RequestsCookieJar(
    requests.cookies.RequestsCookieJar, http.cookiejar.MozillaCookieJar
):
    r"""
    A cookiejar implemented from RequestsCookieJar & MozillaCookieJar
    Supporting features to load/save cookies from/to `cookies.txt`
    """

    def load(
        self, domain="", filename=None, ignore_discard=False, ignore_expires=False
    ):
        super(RequestsCookieJar, self).load(filename, ignore_discard, ignore_expires)

    def save(self, filename=None, ignore_discard=False, ignore_expires=False):
        super(RequestsCookieJar, self).save(filename, ignore_discard, ignore_expires)

    def _really_load(self, f, filename, ignore_discard, ignore_expires):
        try:
            super()._really_load(f, filename, ignore_discard, ignore_expires)
        except:
            pass

    def clear(self, domain=None, path=None, name=None):
        for d in self.list_domains():
            if domain and not d.endswith(domain):
                continue
            super().clear(domain=d, path=path, name=name)


class LeetCodeSession(requests.Session):
    r"""
    Multi-domain cookies persistable session so as to request
    `leetcode.com` / `leetcode-cn.com` within ONE session
    """

    def __init__(self, filename: str = "", only_domain: str = ""):
        super().__init__()
        self.cookies = RequestsCookieJar()
        self.logger = logging.getLogger("leetcode.requester.LeetCodeSession")
        self.headers.update({"User-Agent": USER_AGENT})
        if only_domain:
            self.accept_domains = {only_domain}
        else:
            self.accept_domains = {DOMAIN, DOMAIN_CN}

        self.cookies.filename = filename if filename else config.COOKIES_FILE
        if self.cookies.filename:
            self.load_cookies()

        if DOMAIN in self.accept_domains and not self.is_signedin():
            self.logger.warning(
                "Leetcode.com Not signed in, you may want to download a "
                "cookies.txt with Chrome Extension cookies.txt"
            )
            self.load_cookies_from_local_browser()
            self.is_signedin()

        if DOMAIN_CN in self.accept_domains and not self.is_signedin_cn():
            self.logger.info(
                "Leetcode-cn.com Not signed in, trying to signin leetcode-cn.com..."
            )
            self.login_cn()

    def load_cookies_from_local_browser(self):
        """By browser_cookies3 """
        for domain in self.accept_domains:
            self.logger.info("Loading cookies from local browser for %s." % (domain,))
            self.cookies.update(browser_cookie3.load(domain_name=domain))

    def load_cookies(self):
        """
        Load from cookies.txt first, if failed, try load from local browser,
        Make sure your browser chrome/firefox is logged in.
        """
        self.logger.info("Loading cookies from: %s" % self.cookies.filename)
        try:
            self.cookies.load()
        except FileNotFoundError as fnf:
            self.logger.error("Load from %s failed: %s " % (self.cookies.filename, fnf))
        except Exception as e:
            self.logger.error("Load from %s failed: %s " % (self.cookies.filename, e))
        finally:
            if len(self.cookies) == 0:
                self.load_cookies_from_local_browser()

    def save_cookies(self):
        if not self.cookies.filename:
            return
        try:
            self.cookies.save()
            self.logger.info("Cookies saved to: %s" % self.cookies.filename)
        except Exception as e:
            self.logger.error(
                "Cookies file Not saved: %s Error: %s" % (self.cookies.filename, e)
            )

    def is_signedin(self):
        self.logger.info("Checking signed in Leetcode.com")
        try:
            user_name = get_problem_stats_all(self).get("user_name")
        except Exception as e:
            self.logger.error("Checking signed in Leetcode.com: %s" % e)
            return False

        signedin = user_name != ""
        if signedin:
            self.logger.info("Leetcode.com signedin successfully: %s" % user_name)
            self.save_cookies()
        else:
            self.cookies.clear(domain=DOMAIN)
        return signedin

    def is_signedin_cn(self):
        self.logger.info("Checking signed in Leetcode-cn.com")
        try:
            user_name = get_cn_problem_stats_all(self).get("user_name") or ""
        except Exception as e:
            self.logger.error("Checking signed in Leetcode-cn.com: %s" % e)
            return False

        signedin = user_name != ""
        if signedin:
            self.logger.info("Leetcode-cn.com signedin successfully: %s" % user_name)
            self.save_cookies()
        else:
            self.cookies.clear(domain=DOMAIN_CN)
        return signedin

    def login(self):
        """ TODO: Try login leetcode.com after fucking recaptcha"""
        return False

    def login_cn(self, username="", password=""):
        username = username or config.LEETCODE_USERNMAE_CN
        password = password or config.LEETCODE_PASSWORD_CN
        assert bool(username) and bool(
            password
        ), "Update LEETCODE_USERNMAE_CN & LEETCODE_PASSWORD_CN in `config_private.py` before login_cn."

        try:
            logged_in = login_cn(self, username, password)
        except Exception as e:
            self.logger.error("Failed to login leetcode-cn.com, errors: %s" % e)
        else:
            if logged_in:
                self.logger.info(
                    "Leetcode-cn.com singned in successfully: %s" % username
                )
                self.save_cookies()
            else:
                self.logger.error(
                    "Failed to login leetcode-cn.com, check your username/password."
                )
            return logged_in
        return False


def dictget(d, k):
    if k in d:
        return d[k]
    for _, _v in d.items():
        if not isinstance(_v, dict):
            continue

        item = dictget(_v, k)
        if bool(item):
            return item


def valid_data(data, name):
    valid_fs = {
        "companyTag": lambda x: bool(dictget(x, "companyTag")),
        "topicTags": lambda x: bool(dictget(x, "questions")),
        "favorites": lambda x: bool(dictget(x, "questions")),
        "problemContent": lambda x: any(
            [bool(dictget(x, "content")), bool(dictget(x, "translatedContent"))]
        ),
        "allTags": lambda x: bool(dictget(x, "allTags")),
        "solutionArticleContent": lambda x: bool(dictget(x, "content")),
    }
    return valid_fs[name](data)
