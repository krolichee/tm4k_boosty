import json
import time
import zoneinfo
from typing import Callable

import requests
from urllib.parse import urlencode

from tm4k.blog import Blog
from tm4k.links.links import getBlogPostQLink
from tm4k.post.field import getPostPublishTs
from tm4k.status_label.status_label import updateStatus
from tm4k.modal import mb

__all__ = ['parseBlog']


class CustomException(Exception):
    pref = ""

    def __init__(self, message=None) -> None:
        super().__init__(type(self).pref + (": "+str(message)) if message else "")
        self.message = message if message else type(self).pref

    def __str__(self):
        return self.message


class AuthError(CustomException):
    pref = "Ошибка авторизации (неавторизованный токен)"


class UnexpecedException(CustomException):
    pref = "Неожиданное исключение"


def isFieldExists(obj, key):
    try:
        _ = obj[key]
        return True
    except KeyError:
        return False

def _raiseCase(err:Exception):
    cases = {
        requests.ConnectionError: lambda e:
        type(e)("Ошибка подключения"),
        json.decoder.JSONDecodeError: lambda e:
        type(e)("Ошибка ответа"),
        # requests.exceptions.JSONDecodeError: lambda e: e,
        # AuthError: lambda e: e,
        # Exception: lambda e: e,
        # TypeError: lambda e: e
    }
    if type(err) in list(cases.keys()):
        raise cases[type(err)](err)
    else:
        raise err

def parseBlog(blog_id, token="", from_ts="") -> Blog:
    """
    :raises json.decoder.JSONDecodeError, requests.ConnectionError
    :param blog_id:
    :param token:
    :param from_ts:
    :return:
    """
    blog_posts_list = []
    base_url = getBlogPostQLink(blog_id)
    params = {'to_ts': int(time.time()), 'limit': 50}
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    if from_ts:
        params['from_ts'] = from_ts
    while True:
        request_url = f"{base_url}?{urlencode(params)}"
        try:
            #todo обработка на основе кода статуса
            resp = requests.get(request_url, headers=headers)
            resp_obj: dict = resp.json()
            if "error" in resp_obj.keys():
                raise AuthError()
            request_posts_list = list(resp_obj["data"])
        except Exception as err:
            _raiseCase(err)

        if not len(request_posts_list):
            break
        blog_posts_list += request_posts_list
        updateStatus(f"Обработано постов: {len(blog_posts_list)}")
        last_post = request_posts_list[-1]
        last_post_ts = getPostPublishTs(last_post) - 1
        params["to_ts"] = last_post_ts
    return Blog(blog_posts_list)
