import json
import os

from .fs import mkdirIfNotExist, buildDirRecu
from tm4k.parse import parseBlog

from tm4k.status_label import updateStatus
from tm4k.messages import *
from tm4k.post.field import *
from ..blog import Blog
from tm4k.modal import mb


def getBlogFilePath(blog_id: str) -> str:
    return getBlogFolderDir(blog_id) + ".boosty.json"


def getBlogFolderDir(blog_id: str) -> str:
    return f"blogs/{blog_id}/"


def checkBlogFileExists(blog_id: str) -> bool:
    path = getBlogFilePath(blog_id)
    abs_path = os.path.abspath(path)
    print(abs_path)
    return os.path.isfile(path)


def openBlogFile(blog_id: str) -> Blog:
    path = getBlogFilePath(blog_id)
    if not checkBlogFileExists(blog_id):
        mb.warn(BLOG_FILE_NOT_EXIST_MESSAGE)
        return Blog(list())
    posts_file = open(path, 'r', encoding='utf-8')
    posts_file_string = posts_file.read()
    posts_file.close()
    return Blog(json.loads(posts_file_string))


def writeBlogToFile(blog:Blog):
    path = getBlogFilePath(blog.blog_id)
    buildDirRecu(path)
    open_method = 'w'
    file = open(path, open_method, encoding='utf-8')
    file.write(json.dumps(blog, ensure_ascii=False))
    updateStatus("Записано в файл")


def warnIfNotFullAccess(blog:Blog):
    if not blog.isAllPostsAccessed():
        mb.warn(NON_AUTH_TOKEN_MESSAGE)
        updateStatus("Нет доступа")


def saveBlog(blog:Blog):
    warnIfNotFullAccess(blog)
    writeBlogToFile(blog)


def parseBlogToFile(blog_id: str, token: str):
    if checkBlogFileExists(blog_id):
        if not mb.ask(BLOG_FILE_EXISTS_REWRITE_QUESTION) == 'yes':
            return
    updateStatus("Начало загрузки блога...")
    blog = parseBlog(blog_id, token)
    saveBlog(blog)


def updateBlog(blog_id:str,token:str):
    cur_blog = openBlogFile(blog_id)
    last_post = cur_blog[0]
    from_ts = getPostPublishTs(last_post) + 1
    new_posts_blog = parseBlog(blog_id, token, from_ts)
    updated_blog = new_posts_blog + cur_blog
    return updated_blog


def refreshBlogFile(blog_id:str,token:str):
    if not checkBlogFileExists(blog_id):
        updateStatus("Файл блога отсутствует")
        parseBlogToFile(blog_id, token)
        return
    updated_blog = updateBlog(blog_id,token)
    saveBlog(updated_blog)
