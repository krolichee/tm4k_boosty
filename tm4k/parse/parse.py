import time
import requests
from urllib.parse import urlencode

from tm4k.blog import Blog
from tm4k.links.links import getBlogPostQLink
from tm4k.post.field import getPostPublishTs
from tm4k.status_label.status_label import updateStatus


def parseBlog(blog_id, token="",from_ts="")->Blog:
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
        resp = requests.get(request_url, headers=headers)
        try:
            request_posts_list = list(resp.json()["data"])
        except:
            print(resp.text)
            raise
        if not len(request_posts_list):
            break
        blog_posts_list += request_posts_list
        updateStatus(f"Обработано постов: {len(blog_posts_list)}")
        last_post = request_posts_list[-1]
        last_post_ts = getPostPublishTs(last_post) - 1
        params["to_ts"] = last_post_ts
    return Blog(blog_posts_list)
