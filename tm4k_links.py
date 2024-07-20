from tm4k_post_field import *


def printPostsLinks(posts_list):
    for post in posts_list:
        print(getPostLink(post))


def getPostEditLink(post_id, blog_id):
    return "https://boosty.to/" + blog_id + "/edit-post/" + post_id


def getPostLinkByStr(post_id: str, blog_id: str):
    return "https://boosty.to/" + blog_id + "/posts/" + post_id


def getPostLink(post: dict):
    return getPostLinkByStr(getPostId(post), getPostBlogId(post))


def getPostApiLink(blog_id:str,post_id:str):
    return 'https://api.boosty.to/v1/blog/'+blog_id + '/post/' + post_id
