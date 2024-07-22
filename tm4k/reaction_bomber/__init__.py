# А тут я баловался. Наставил мыши лайков на посты

import time

from tm4k.fs.blog_file import *
import requests

blog_id = "marcykatya"
token = ""

posts_list = openBlogFile(blog_id)

# "reactions": {
#                 "heart": 6,
#                 "sad": 0,
#                 "fire": 2,
#                 "angry": 0,
#                 "wonder": 0,
#                 "dislike": 0,
#                 "laught": 0,
#                 "like": 0
#             },

data = {
    'reaction': 'heart'
}
headers = {'Authorization':
               f'Bearer {token}'}

links = []
for post in posts_list:
    url = f"https://api.boosty.to/v1/blog/marcykatya/post/" + post["id"] + "/reaction?from_page=blog"
    print(post["id"])
    print(requests.post(url, data, headers=headers).text)
    time.sleep(0.1)
