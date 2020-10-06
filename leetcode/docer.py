""" Doc Leetcode
1. Get or make a dir /path/to/basedir/0001_two-sum/ for example;
2. Generate a readme based on problem'contents and write to 0001_two-sum/README.[org|md];
3. Generate solution articles based on solutions list, ./articles/两数之和/README.[org|md];
4. Generate solution.lang(solution_test.lang if possible, for yourself)
   based on code snippet and example test cases.
   For example: ./solutions/solution.go & ./solutions/solution_test.go

P.S Read code instead of edoc
"""

import argparse
import copy
import json
import logging
import pathlib
import re
import subprocess
from datetime import datetime

import dateparser
import pymongo
import pypandoc

from leetcode import config

logger = logging.getLogger(__name__)


def slugify(value, allow_unicode=True):
    r""" Copied from `django.utils.text` """
    import unicodedata

    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower()).strip()
    return re.sub(r"[-\s]+", "-", value)


def get_question_frontend_id(question_id: str) -> str:
    """
    1 -> 0001
    A1 -> A1
    """
    try:
        question_id = int(question_id)
        question_id_str = f"{question_id:04}"
    except ValueError:
        question_id_str = question_id
    return question_id_str


def get_or_mk_question_dir(question_id: str, title_slug: str, base_dir: str) -> str:
    """
    The base directory: /path/to/your/leetcode/
    The question directory: /path/to/your/leetcode/0001-two-sum/
    """
    question_id_str = slugify(get_question_frontend_id(question_id))
    dirname = f"{question_id_str}_{title_slug}"
    question_dir = pathlib.Path(base_dir).resolve().joinpath(dirname)
    if not question_dir.exists():
        question_dir.mkdir()

    return question_dir


def write_question_json(filepath: str, data: dict) -> str:
    with open(filepath, "w") as fp:
        s = json.dumps(data)
        fp.write(s)

    return filepath


def pandoc_html2org(html_text: str) -> str:
    output = pypandoc.convert_text(html_text, "org", format="html")
    return output


def pandoc_md2org(md_text: str) -> str:
    output = pypandoc.convert_text(md_text, "org", format="markdown")
    return output


"""
Read content from question data and generate org/md README file
"""

ORG_TEMPLATE = """#+TITLE: {title}
#+DATE: {create_date}
#+LAST_MODIFIED: {last_modified}
#+STARTUP: overview
#+HUGO_WEIGHT: auto
#+HUGO_AUTO_SET_LASTMOD: t
#+EXPORT_FILE_NAME: {title_slug}
#+HUGO_BASE_DIR:{hugo_basedir}
#+HUGO_SECTION: {hugo_section}
#+HUGO_CATEGORIES:{hugo_category}
#+HUGO_TAGS: {tags}

{content}
"""

BASE_URL = "https://leetcode.com/"
CN_BASE_URL = "https://leetcode-cn.com/"


def update_last_modified(content: str):
    last_modified_re = re.compile("(#\+LAST_MODIFIED:)(.*)")
    content = last_modified_re.sub(
        f"\g<1> {datetime.now().strftime('%Y-%m-%d %H:%M')}", content
    )
    return content


def reformat_tag_name_display(tag_name: str) -> str:
    tag_name = tag_name.replace(" ", "").replace("-", "")
    return tag_name


def write_cn_problems_list_org_readme(problems: list, filepath: str) -> str:
    """
    Write all TODO problems to org doc, such as leetcode/README.org
    Update if problems list updated.
    """
    orgfile = pathlib.Path(filepath).resolve()
    headlines = list()

    if orgfile.exists():
        with orgfile.open("r") as fp:
            orgcontent = fp.read().strip()
        orgcontent = update_last_modified(orgcontent)
        if not orgcontent.endswith("\n"):
            orgcontent += "\n"
    else:
        data = {
            "create_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "title": "Leetcode-cn Problems List",
            "title_slug": "leetcode-cn-problems-list",
            "hugo_basedir": "~/G/blog",
            "hugo_section": "leetcode",
            "hugo_category": "leetcode",
            "tags": "Leetcode Algorithms",
            "content": """* Problems List\n:PROPERTIES:\n:VISIBILITY: children\n:END:\n""",
        }
        orgcontent = ORG_TEMPLATE.format(**data)

    for p in problems:
        title_slug = p["titleSlug"]
        if title_slug in orgcontent:
            continue

        link = f"https://leetcode-cn.com/problems/{p['titleSlug']}/"
        title = f"{p['questionFrontendId']}. {p['title']}"
        tags = ""
        if p.get("topicTags", []):
            tags = f":{':'.join([reformat_tag_name_display(t['name']) for t in p['topicTags']])}:"

        headline = f"** TODO [[{link}][{title}]] {tags}"
        headlines.append(headline)

    orgcontent += "\n".join(headlines)
    with orgfile.open("w") as fp:
        fp.write(orgcontent)

    return filepath


def get_org_link_display(
    frontend_id: str, title: str, slug: str, cn: bool = True
) -> str:
    linkbase = CN_BASE_URL if cn else BASE_URL
    link = f"{linkbase}problems/{slug}/"
    name = f"{get_question_frontend_id(frontend_id)}. {title}"
    orglink = f"[[{link}][{name}]]"
    return orglink


def get_hints_org_display(hints: list) -> str:
    if not hints:
        return ""

    hints = "** Hints\n" + "\n".join([f"{i+1}. {h}" for i, h in enumerate(hints)])
    return hints


def get_tags_org_link_display(slug: str, name: str, cn: bool) -> str:
    tag_linkbase = f"{CN_BASE_URL}tag/" if cn else f"{BASE_URL}tag/"
    return f"[[{tag_linkbase}{slug}/][{name}]]"


def get_tags_org_display(tags: list, cn: bool) -> str:
    if not tags:
        return ""

    tags_display = "** Topic Tags\n"
    for i, t in enumerate(tags):
        tags_display += f"{i+1}. {get_tags_org_link_display(t['slug'], t['translatedName'] if cn else t['name'], cn)}\n"
    return tags_display


def get_cn_frontend_id_from_statsall(slug: str) -> str:
    client = pymongo.MongoClient()
    stats = client.leetcode_cn.problem_stats.find_one({"question__title_slug": slug})
    if stats:
        return stats["frontend_question_id"]
    return ""


def get_similar_problems_display(similar_problems: list, cn: bool) -> str:
    if not similar_problems:
        return ""

    ret = list()
    for problem in similar_problems:
        slug = problem.get("titleSlug")
        title = problem.get("translatedTitle") if cn else problem.get("title")
        frontend_id = get_cn_frontend_id_from_statsall(slug)
        org_link = get_org_link_display(frontend_id, title, slug, cn)
        ret.append("*** " + org_link)

    return "** Similar Problems\n" + "\n".join(ret)


def get_related_company_display(companies: dict) -> str:
    if not companies:
        return ""

    companies = sorted(companies.items())
    ret = list()
    for k, tags in companies:
        for company in tags["tags"]:
            slug = company.get("slug")
            name = company.get("name")
            times = company.get("timesEncountered")
            link = f"https://leetcode-cn.com/company/{slug}/"
            ret.append(f"*** {k}. [[{link}][{name}]] * {times}")

    return "** Companies\n" + "\n".join(ret)


def get_problem_content_display(problem: dict, cn: bool) -> str:
    nl = "\n"
    frontend_id = problem.get("questionFrontendId")
    title = problem.get("translatedTitle") if cn else problem.get("title")
    slug = problem.get("titleSlug")
    difficulty = problem.get("difficulty")
    likes, dislikes = problem.get("likes"), problem.get("dislikes")
    ac_rate = json.loads(problem.get("stats")).get("acRate")
    frequency = problem.get("stat", {}).get("frequency", 0)
    hints = problem.get("hints", [])
    tags = problem.get("topicTags")
    similar_problems = json.loads(problem.get("similarQuestions", "[]"))
    companies = json.loads(problem.get("companyTagStats", "{}"))
    content = problem.get("translatedContent") if cn else problem.get("content")
    if not content:
        return ""

    contentorg = f"""* {get_org_link_display(frontend_id, title, slug, cn)}
:PROPERTIES:
:VISIBILITY: {'folded' if cn else 'children'}
:END:

#+begin_quote
{difficulty} U:{likes} D:{dislikes} AC:{ac_rate} F:{frequency}
#+end_quote

{pandoc_html2org(content)}

{get_hints_org_display(hints)}
{get_tags_org_display(tags, cn)}
{get_similar_problems_display(similar_problems, cn)}
{get_related_company_display(companies)}"""
    return contentorg


def strip_blank_lines(content: str) -> str:
    nlre = re.compile("([\n][\n]{2,})")
    content = nlre.sub("\n", content)
    return content


def write_problem_org_readme(problem: dict, filepath: str) -> str:
    orgfile = pathlib.Path(filepath).resolve()

    if orgfile.exists():
        with orgfile.open("r") as fp:
            orgcontent = fp.read()
        orgcontent = update_last_modified(orgcontent)
    else:
        content = get_problem_content_display(problem, False)
        translated_content = get_problem_content_display(problem, True)
        data = {
            "create_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "title": f"{get_question_frontend_id(problem['questionFrontendId'])}. {problem['title']}",
            "title_slug": f"{get_question_frontend_id(problem['questionFrontendId']).lower().replace(' ', '-')}-{problem['titleSlug']}",
            "hugo_basedir": "~/G/blog",
            "hugo_section": "leetcode",
            "hugo_category": "leetcode",
            "tags": f"Leetcode Algorithms {' '.join(reformat_tag_name_display(x['name']) for x in problem['topicTags'])}",
            "content": f"{content}\n{translated_content}",
        }
        orgcontent = ORG_TEMPLATE.format(**data)

    orgcontent = strip_blank_lines(orgcontent)
    with orgfile.open("w") as fp:
        fp.write(orgcontent)

    return filepath


"""
TODO: Markdown doc
"""


def generate_md_doc(question: dict) -> str:
    # TODO: For boys and girls who're using wtf md in 0202
    # print(html2markdown.convert(question["content"]))
    pass


"""
TODO: Solution Articles
"""


def stripe_code_block_tagid(content: str) -> str:
    """
    ```java [rkfa5BFX-Java]
    ```
    """
    tagid_re = re.compile("(```[\w\d+]+)( ?\[.*\])")
    content = tagid_re.sub("\g<1>", content)
    return content


def generate_cn_problem_solution_org(solution: dict):
    question_frontend_id = solution["frontend_question_id"]
    question_title = solution["question_title"]
    question_slug = solution["question_slug"]
    solution_slug = solution["slug"]
    solution_url = (
        f"https://leetcode-cn.com/problems/{question_slug}/solution/{solution_slug}/"
    )
    title = solution["title"]
    tags = solution["tags"]
    author = solution["author"]
    content = stripe_code_block_tagid(solution["content"])

    content_head = f"""* [[{solution_url}][{title}]]{' :' if tags else ''}{':'.join([t['name'].replace(' ', '') for t in tags])}{':' if tags else ''}
:PROPERTIES:
:VISIBILITY: children
:END:

#+begin_quote
[[https://leetcode-cn.com/problems/{question_slug}/][{get_question_frontend_id(question_frontend_id)}. {question_title}]] [[{solution_url}][{title}]] solution by [[https://leetcode-cn.com/u/{author['profile']['userSlug']}/][{author['username']}]]
#+end_quote
"""
    data = {
        "create_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "title": title,
        "title_slug": f"{get_question_frontend_id(question_frontend_id)}-{question_slug}-{solution_slug}",
        "hugo_basedir": "~/G/blog",
        "hugo_section": "leetcode",
        "hugo_category": "leetcode",
        "tags": f"Leetcode Algorithms{' ' if tags else ''}{' '.join([reformat_tag_name_display(t['name']) for t in tags])}",
        "content": content_head,
    }
    orghead = ORG_TEMPLATE.format(**data)
    orgcontent = pandoc_md2org(content)
    sub_headline_re = re.compile("(^\*{2,})( .*)")
    split_line_re = re.compile("[\-]{3,}")
    orglines = list()
    for line in orgcontent.split("\n"):
        if sub_headline_re.findall(line):
            orglines.append(sub_headline_re.sub("**\g<2>", line))
        elif split_line_re.findall(line):
            orglines.append("\n")
        else:
            orglines.append(line)

    return strip_blank_lines(orghead + "\n".join(orglines))


def generate_cn_problem_solution_md(solution: dict):
    question_frontend_id = solution["frontend_question_id"]
    question_title = solution["question_title"]
    question_slug = solution["question_slug"]
    solution_slug = solution["slug"]
    solution_url = (
        f"https://leetcode-cn.com/problems/{question_slug}/solution/{solution_slug}/"
    )
    title = solution["title"]
    tags = solution["tags"]
    author = solution["author"]
    content = stripe_code_block_tagid(solution["content"])
    q = '"'
    create_date = dateparser.parse(solution["createdAt"]).strftime(
        "%Y-%m-%dT%H:%M:%S+08:00"
    )
    meta = f""""+++
title = "{get_question_frontend_id(question_frontend_id)}. {question_title} {title} "
author = ["{author['username']}"]
date = {create_date}
tags = ["Leetcode", "Algorithms", {f"{', '.join([q + reformat_tag_name_display(t['name']) + q for t in tags])}"}]
categories = ["leetcode"]
draft = false
+++\n\n"""
    headline = f"""# {title}

> [{get_question_frontend_id(question_frontend_id)}. {question_title}](https://leetcode-cn.com/problems/{question_slug}/)
> [{title}]({solution_url}) by [{author['username']}](https://leetcode-cn.com/u/{author['profile']['userSlug']}/)

"""
    return strip_blank_lines(meta + headline + content)


def write_problem_solution_articles(solutions: list, problem_dir: str):
    articles_dir = pathlib.Path(problem_dir).resolve().joinpath("article")
    if not articles_dir.exists():
        articles_dir.mkdir()

    for solution in solutions:
        title = solution["title"]
        by_leetcode = solution["byLeetcode"]
        solution_dir = articles_dir.joinpath(
            f"{slugify(title)}{' By Leetcode' if by_leetcode else ''}"
        )
        if not solution_dir.exists():
            solution_dir.mkdir()

        article_readme = solution_dir.joinpath("README.md")
        article_readme_org = solution_dir.joinpath("README.org")
        with article_readme.open("w") as fp:
            fp.write(generate_cn_problem_solution_md(solution))

        with article_readme_org.open("w") as fp:
            fp.write(generate_cn_problem_solution_org(solution))


"""
Write code snippets and generate tests.
TODO: Examples(if avaiable) to go testcase
"""


def generate_solution_code_golang(problem):
    """ Generate solution.go based on problem["snippets"]"""
    ret = "package solution\n\n{}"
    gocode = list(filter(lambda x: x["langSlug"] == "golang", problem["codeSnippets"]))
    if not gocode:
        raise Exception("Go code snippets not found")

    # Insert extra var ret, return ret code inside the func block
    return_type_re = re.compile("\) (.*) \{")
    func_block_re = re.compile("\{\n.*\n\}")
    return_type = return_type_re.findall(gocode[0]["code"])[0]
    block = "{\n\tvar ret %s\n\treturn ret \n}" % return_type

    return ret.format(func_block_re.sub(block, gocode[0]["code"]))


def generate_test_case_golang(filepath):
    testcase_re = re.compile("// TODO: Add test cases.")
    testfile = pathlib.Path(filepath).resolve()
    if not testfile.exists():
        return

    with testfile.open("r") as fp:
        tests = fp.read()

    cases = '{"Example 1", args{}, },'
    tests = testcase_re.sub(cases, tests)
    with testfile.open("w") as fp:
        fp.write(tests)
    return tests


def generate_test_golang(filepath: str, force_write: bool = False):
    gofilepath = pathlib.Path(filepath).resolve()
    testfile = gofilepath.parent.joinpath(f"{gofilepath.name.strip('.go')}_test.go")

    if not force_write and testfile.exists():
        print("Already Exists:", testfile)
        return testfile

    subprocess.check_call(["gotests", "-all", "-w", gofilepath])
    generate_test_case_golang(testfile)

    return testfile


def write_solution_file(
    lang: str,
    solution_code: str,
    problem_dir: str,
    solution_dirname: str = "solution",
    solution_filename: str = "solution",
    force_write: bool = False,
):
    """ Write the solution code to specific solution.lang file"""
    solution_dir = pathlib.Path(problem_dir).resolve().joinpath(solution_dirname)
    if not solution_dir.exists():
        solution_dir.mkdir()

    solution_file = solution_dir.joinpath(f"{solution_filename}.{lang}")
    if not force_write and solution_file.exists():
        print("Already Exists:", solution_file)
        return solution_file

    with solution_file.open("w") as fp:
        fp.write(solution_code)

    return solution_file


def get_leetcode_basedir():
    path = pathlib.Path(config.LEETCODE_BASEDIR).expanduser().resolve()
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        logger.debug("Mkdir %s" % path)
    return path


def get_problems_list_from_mongo() -> list:
    client = pymongo.MongoClient()
    problems = client.leetcode_cn.problems.find({}, sort=[("question_id", 1)])
    return list(problems)


def get_problem_from_mongo(slug: str) -> dict:
    client = pymongo.MongoClient()
    problem = client.leetcode_cn.problems.find_one(
        {"$or": [{"titleSlug": slug}, {"questionFrontendId": slug}]}
    )
    return problem


def get_problem_solutions_from_mongo(slug: str) -> list:
    client = pymongo.MongoClient()
    solutions = client.leetcode_cn.solutions.find(
        {"$or": [{"question_slug": slug}, {"frontend_question_id": slug}]}
    )
    return list(solutions)


# TODO: Do get from leetcode.com instead of mongo
if __name__ == "__main__":
    basedir = get_leetcode_basedir()
    problems = get_problems_list_from_mongo()
    write_cn_problems_list_org_readme(
        problems, pathlib.Path(basedir).joinpath("README.org")
    )

    parser = argparse.ArgumentParser(
        description="For auto generate doc of question from leetcode-cn.com",
        usage="python3 leetcode.py slug/id",
    )
    parser.add_argument(
        "slugs", type=str, nargs="+", help="Question slug to get",
    )
    args = parser.parse_args()

    for slug in args.slugs:
        slug = slug.strip()
        problem = get_problem_from_mongo(slug)
        if not problem:
            print("Not Found:", slug)
            continue

        basedir = get_leetcode_basedir()
        frontend_id = problem["questionFrontendId"]
        title_slug = problem["titleSlug"]
        problem_dir = get_or_mk_question_dir(frontend_id, title_slug, basedir)

        # README.org
        orgreadme_path = problem_dir.joinpath("README.org")
        # TODO: separate -cn from leetcode
        write_problem_org_readme(problem, orgreadme_path)

        # Personal solution file
        solution_file = write_solution_file(
            lang="go",
            solution_code=generate_solution_code_golang(problem),
            problem_dir=problem_dir,
        )
        generate_test_golang(solution_file)

        #  Solution Articles
        solutions = get_problem_solutions_from_mongo(slug)
        write_problem_solution_articles(solutions, problem_dir)
