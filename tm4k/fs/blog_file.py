import json
import os
from functools import wraps

from .fs import buildDirRecu

from tm4k.status_label import updateStatus
from tm4k.messages import *
from tm4k.blog import Blog
from tm4k.modal import mb



def getBlogFilePath(blog_id: str) -> str:
    return getBlogFolderDir(blog_id) + ".boosty.json"


def getBlogFolderDir(blog_id: str) -> str:
    return f"local/blogs/{blog_id}/"


def isBlogFileExists(blog_id: str) -> bool:
    path = getBlogFilePath(blog_id)
    abs_path = os.path.abspath(path)
    return os.path.isfile(abs_path)


def openBlogFile(blog_id: str) -> Blog:
    path = getBlogFilePath(blog_id)
    if not isBlogFileExists(blog_id):
        mb.warn(BLOG_FILE_NOT_EXIST_MESSAGE)
        return list()
    file = open(path, 'r', encoding='utf-8')
    posts_file_string = file.read()
    file.close()
    return Blog(json.loads(posts_file_string))


def writeBlogToFile(blog: Blog):
    path = getBlogFilePath(blog.blog_id)
    buildDirRecu(path)
    open_method = 'w'
    file = open(path, open_method, encoding='utf-8')
    file.write(json.dumps(blog, ensure_ascii=False))
    print(os.path.abspath(path))
    updateStatus("Записано в файл")


def warnIfNotFullAccess(blog: Blog):
    if not blog.isAllPostsAccessed():
        mb.warn(NON_AUTH_TOKEN_MESSAGE)
        updateStatus("Нет доступа")


def saveBlog(blog: Blog):
    warnIfNotFullAccess(blog)
    writeBlogToFile(blog)


