from tm4k_links import getPostLink
from tm4k_post_field import hasTags


def filterAllTaggedPosts(posts_list):
    return list(filter(lambda x: hasTags(x), posts_list))


def printAllTaggedPosts(posts_list: list, blog_id: str):
    all_tagged_posts = filterAllTaggedPosts(posts_list)
    for post in all_tagged_posts:
        print(getPostLink(post))
