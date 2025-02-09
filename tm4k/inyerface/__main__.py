import inspect
from functools import wraps

from tm4k.status_label import *

from tm4k.wb.commands import *

from tm4k.fs import *

import os.path

import tkinter
from tkinter import *
from tkinter import ttk

from config import token as cfg_token, blog_id as cfg_blog_id
from typing import Callable, Any

from tm4k.wb.commands import refreshBlogFile, parseBlogToFile
from tm4k.wb.df_utils import mergeMatrixPostsOnly

import tm4k.fs.file_exists_dep as dep

blog_id = cfg_blog_id
token = cfg_token

#script_dir = os.path.dirname(os.path.abspath(__file__))
#os.chdir(script_dir)


def setEntryText(entry: tkinter.Entry, text):
    entry.delete(0, tkinter.END)
    entry.insert(0, text)


root = Tk()

setModalRoot(root)

frm_h = ttk.Frame(root, padding=10)
frm_h.grid()
frm = ttk.Frame(root, padding=10)
frm.grid()

blogid_entry = ttk.Entry(frm_h, validate="all")
setEntryText(blogid_entry, cfg_blog_id)

token_entry = ttk.Entry(frm_h, validate="all")
setEntryText(token_entry, cfg_token)

status_label = ttk.Label(frm, text="", foreground="dark gray")
setStatusLabel(status_label)


def exc_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            mb.err(str(e))
            updateStatus(str(e), 'err')
            raise e

    return wrapper


def pass_params(func, par_dict: dict[str:Any]):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for k, v in par_dict.items():
            if hasParameter(func, k):
                kwargs[k] = v
        return func(*args, **kwargs)

    return wrapper


def hasParameter(func, par_name):
    signature = inspect.signature(func)
    parameters = signature.parameters
    return par_name in parameters.keys()


def pass_credentials(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return pass_params(func, {
            'blog_id': blogid_entry.get(),
            'token': token_entry.get()
        })(*args, **kwargs)

    return wrapper


def setActiveIf(ctr, b_val):
    states = {
        True: 'normal',
        False: 'disabled'
    }
    ctr.config(state=states[b_val])


blog_file_path = pass_credentials(getBlogFilePath)()
tags_file_path = pass_credentials(getTagsFilePath)()

dep.newPath(blog_file_path, setActiveIf)
dep.newPath(tags_file_path, setActiveIf)


def bfe_dep(bt: ttk.Button):
    dep.newDep(blog_file_path, bt)
    return bt


def tfe_dep(bt: ttk.Button):
    dep.newDep(tags_file_path, bt)
    return bt


def tm4k_command(func):
    @exc_handler
    @dep.updating_fe_dep
    @pass_credentials
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def createTm4kButton(text: str, command: Callable, form=frm, is_active: bool = True):
    return ttk.Button(form, text=text, command=tm4k_command(command))


blogfile_label = ttk.Label(frm, text="Файл блога")
tagfile_label = ttk.Label(frm, text="Файл тегов")
publish_label = ttk.Label(frm, text="Публикация")
additional_label = ttk.Label(frm, text="Доп. функции")

sect_labels = [blogfile_label, tagfile_label, publish_label, additional_label]

try:
    children = [
        [ttk.Label(frm_h, text="Id блога"), blogid_entry],
        [ttk.Label(frm_h, text="Токен авторизации"), token_entry],
        [blogfile_label],
        [
            createTm4kButton("Загрузить", parseBlogToFile),
            bfe_dep(createTm4kButton("Обновить", refreshBlogFile))],
        [tagfile_label],
        [bfe_dep(createTm4kButton("Получить", importTagsFileByBlogId)),
         tfe_dep(createTm4kButton("Обновить", lambda: refreshTagFile(blog_id)))],
        [publish_label],
        [tfe_dep(createTm4kButton("Опубликовать новые теги из файла тегов",
                                  lambda: publish(blog_id, token)))],
        [additional_label],
        [tfe_dep(createTm4kButton("RestoreTS",
                                  lambda: (restoreTs(blog_id),
                                           startfileTagsFile(blog_id)), is_active=isTagsFileExists(blog_id)))],
        [tfe_dep(createTm4kButton("merge",
                                  lambda: mergeMatrixPostsOnly(blog_id), is_active=isTagsFileExists(blog_id)))],
        [status_label]
    ]
except Exception as err:
    print("exc")
    print(err)
    raise err


def formatGrid():
    max_column_number = 0
    for row in children:
        row_len = len(row)
        if row_len > max_column_number:
            max_column_number = row_len

    for i in range(len(children)):
        for j in range(len(children[i])):
            if children[i][j] not in sect_labels:
                children[i][j].grid(row=i, column=j, columnspan=int(max_column_number / len(children[i])), sticky="we"
                                    , pady=2)
            else:
                children[i][j].grid(row=i, column=0, columnspan=int(max_column_number / len(children[i])), sticky="sw"
                                    , pady=(10, 0))


formatGrid()
status_label.config(wraplength='250')

root.mainloop()
