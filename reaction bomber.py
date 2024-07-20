#А тут я баловался. Наставил мыши лайков на посты

import time

from tm4k_file_blog import *
import requests
posts_list = openPostsList("marcykatya")

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
'Bearer 506b1ecdc473a8dcc770684889c7de2963846ebb39738f0978a776b743c80203'}

url = "https://api.boosty.to/v1/blog/marcykatya/post/6dbbb6a6-a476-4960-8a92-518fc052205b/reaction?from_page=blog"

requests.post(url,data,headers=headers)

from main import stuck


stuck()

links = []
for post in  posts_list:
 url = "https://api.boosty.to/v1/blog/marcykatya/post/"+post["id"]+"/reaction?from_page=blog"
 print(post["id"])
 print(requests.post(url, data, headers=headers).text)
 time.sleep(0.1)


