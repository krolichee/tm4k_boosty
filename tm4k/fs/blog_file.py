import json
import os

from .fs import mkdirIfNotExist, buildDirRecu
from tm4k.parse import parseBlog

from tkinter import messagebox
from tm4k.status_label import updateStatus
from tm4k.messages import *


#todo обновление файла блога новыми постами
def getBlogFilePath(blog_id: str) -> str:
    return getBlogFolderDir(blog_id) + ".boosty.json"


def getBlogFolderDir(blog_id: str) -> str:
    return f"blogs/{blog_id}/"


def checkBlogFileExists(blog_id: str) -> bool:
    path = getBlogFilePath(blog_id)
    abs_path = os.path.abspath(path)
    print(abs_path)
    return os.path.isfile(path)


def openPostsList(blog_id: str) -> list:
    path = getBlogFilePath(blog_id)
    if not checkBlogFileExists(blog_id):
        messagebox.showwarning("!!", BLOG_FILE_NOT_EXIST_MESSAGE)
        return list()
    posts_file = open(path, 'r', encoding='utf-8')
    posts_file_string = posts_file.read()
    posts_file.close()
    return json.loads(posts_file_string)



def postsListToFile(posts_list: list, blog_id: str):
    path = getBlogFilePath(blog_id)
    buildDirRecu(path)


    open_method = 'w'
    file = open(path, open_method, encoding='utf-8')
    file.write(json.dumps(posts_list, ensure_ascii=False))
    updateStatus("Записано в файл")


def blogToFile(blog_id: str, token: str):
    if checkBlogFileExists(blog_id):
        if not messagebox.askquestion("??", BLOG_FILE_EXISTS_REWRITE_QUESTION, icon='warning') == 'yes':
            return
    updateStatus("Начало загрузки блога...")
    blog_posts = parseBlog(blog_id, token)
    for post in blog_posts:
        if not post['hasAccess']:
            # todo
            messagebox.showwarning("!!", NON_AUTH_TOKEN_MESSAGE)
            updateStatus("Нет доступа")
            break

    postsListToFile(blog_posts, blog_id)
