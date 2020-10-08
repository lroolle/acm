from .tasks import *


@shared_task(bind=True, base=LeetcodeBaseTask)
def test_autoretry_for_request_exception(self):
    raise RequestException("A RequestException raised.")


@shared_task(bind=True, base=LeetcodeBaseTask)
def test_autoretry_for_badrequeste_xception(self):
    from leetcode.requester import BadRequest

    raise BadRequest("A BadRequest exception raised.")


@shared_task(bind=True, base=LeetcodeBaseTask)
def test_autoretry_for_notauthenticated_exception(self):
    from leetcode.requester import NotAuthenticated

    raise NotAuthenticated("A NotAuthenticated exception raised.")
