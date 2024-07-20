import requests
import urllib.parse
import time

from tm4k_post_field import getPostTs
from tm4k_status import updateStatus


def parseBlog(blog_id, token=""):
    r"""GET blog list
    :return:
    :rtype: list
    """
    posts_count = 0
    blog_posts_list = []
    boosty_blog_api_domain = "https://api.boosty.to/v1/blog/"
    request_domain = boosty_blog_api_domain + blog_id + "/post/?"
    params = {'to_ts': int(time.time()),'limit':50}
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    while True:
        request_url = request_domain + urllib.parse.urlencode(params)
        resp = requests.get(request_url, headers=headers)
        print(resp.status_code)
        request_posts_list = list(resp.json()["data"])
        if not len(request_posts_list):
            break
        blog_posts_list += request_posts_list
        updateStatus(f"Обработано постов: {len(blog_posts_list)}")
        last_post = request_posts_list[-1]
        last_post_ts = getPostTs(last_post) - 1
        params["to_ts"] = last_post_ts
    return blog_posts_list







