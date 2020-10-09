import random

import requests

from .tasks import *


@shared_task(bind=True, base=LeetcodeSessionBaseTask)
def test_autoretry_for_request_exception(self):
    raise RequestException("A RequestException raised.")


@shared_task(bind=True, base=LeetcodeSessionBaseTask)
def test_autoretry_for_badrequeste_exception(self):
    from leetcode.requester import BadRequest

    raise BadRequest("A BadRequest exception raised.")


@shared_task(bind=True, base=LeetcodeSessionBaseTask)
def test_autoretry_for_notauthenticated_exception(self):
    from leetcode.requester import NotAuthenticated

    raise NotAuthenticated("A NotAuthenticated exception raised.")


@shared_task(bind=True, max_retries=5, base=LeetcodeSessionBaseTask)
def test_autoretry_for_timeout_exception(self):
    n = random.randint(0, 10)
    if n > 8:
        raise requests.exceptions.Timeout("A Timeout exception raised.")


@shared_task(bind=True, base=LeetcodeSessionBaseTask)
def test_autoretry_for_connectionerror_exception(self, *args):
    raise requests.exceptions.ConnectionError("A ConnectionError exception raised.")


def test_autoretry_for_chain():
    flow = (
        test_autoretry_for_timeout_exception.s()
        | test_autoretry_for_connectionerror_exception.s()
        | test_autoretry_for_request_exception.s()
        | test_autoretry_for_notauthenticated_exception.s()
        | test_autoretry_for_badrequeste_exception.s()
    )()
    return flow
