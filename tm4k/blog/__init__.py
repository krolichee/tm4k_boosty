from importlib.metadata import DeprecatedList
from typing import Iterable

from tm4k.post.field import *

__all__ = ['Blog']


def isAllBlogIdCommon(posts_list):
    blog_id = getPostBlogId(posts_list[0])
    for post in posts_list[1:]:
        if getPostBlogId(post) != blog_id:
            return False
    return True


class Blog(DeprecatedList,Iterable):
    def __init__(self, posts_list: list):
        super().__init__(posts_list)
        if not isAllBlogIdCommon(self):
            raise ValueError("Posts has not common blog_id")
        self.blog_id = getPostBlogId(posts_list[0])

    def isAllPostsAccessed(self):
        for post in self:
            if not post['hasAccess']:
                return False
        else:
            return True

