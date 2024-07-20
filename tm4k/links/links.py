from tm4k.post.field import *


def printPostsLinks(posts_list):
    for post in posts_list:
        print(getPostLink(post))


def getPostEditLink(post_id, blog_id):
    return f"https://boosty.to/{blog_id}/edit-post/{post_id}"


def getPostLinkByStr(post_id: str, blog_id: str):
    return f"https://boosty.to/{blog_id}/posts/{post_id}"


def getPostLink(post: dict):
    return getPostLinkByStr(getPostId(post), getPostBlogId(post))


def getBlogApiLink(blog_id):
    return f"https://api.boosty.to/v1/blog/{blog_id}"


def getBlogPostQLink(blog_id: str):
    return f"https://api.boosty.to/v1/blog/{blog_id}/post/"


def getPostApiLink(blog_id: str, post_id: str):
    return f"https://api.boosty.to/v1/blog/{blog_id}/post/{post_id}"
