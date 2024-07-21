import json
import os

from .fs import mkdirIfNotExist, buildDirRecu
from tm4k.parse import parseBlog

from tkinter import messagebox
from tm4k.status_label.status_label import updateStatus


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
        messagebox.showwarning("!!", "Файл блога не существует")
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
    """
    :param blog_id:
    :type blog_id: str
    :type token: str
    """
    # print(os.path.abspath(os.curdir))
    # time.sleep(1)
    if checkBlogFileExists(blog_id):
        if not messagebox.askquestion("??", "Файл блога уже существует. Продолжить?", icon='warning') == 'yes':
            return
    updateStatus("Начало загрузки блога...")
    blog_posts = parseBlog(blog_id, token)
    for post in blog_posts:
        if not post['hasAccess']:
            # todo
            messagebox.showwarning("!!", "Указанный токен не позволяет получить доступ ко всем постам. "
                                         "Содержимое .boosty файла будет неполным"
                                         "\nТакже неавторизованный токен не позволит загрузить теги")
            updateStatus("Нет доступа")
            break

    postsListToFile(blog_posts, blog_id)
