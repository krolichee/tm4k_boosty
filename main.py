import tm4k.modal.config as modal_cfg
import tm4k.status_label.config as status_cfg

from tm4k.wb.commands import *

import os.path

import tkinter
from tkinter import *
from tkinter import ttk

from config import token as cfg_token,blog_id as cfg_blog_id

blog_id = cfg_blog_id
token = cfg_token


script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


def setEntryText(entry: tkinter.Entry, text):
    entry.delete(0, tkinter.END)
    entry.insert(0, text)


root = Tk()

modal_cfg.setRoot(root)

frm = ttk.Frame(root, padding=10)
frm.grid()

blogid_entry = ttk.Entry(frm, validate="all")
setEntryText(blogid_entry, cfg_blog_id)

token_entry = ttk.Entry(frm, validate="all")
setEntryText(token_entry, cfg_token)

status_label = ttk.Label(frm, text="", foreground="dark gray")
status_cfg.setLabel(status_label)


def updateBlogId(_):
    global blogid_entry
    global blog_id
    blog_id=blogid_entry.get()


def updateToken(_):
    global token_entry
    global token
    token = token_entry.get()

blogid_entry.bind("<KeyRelease>", updateBlogId)
token_entry.bind("<KeyRelease>",updateToken)

children = [
    [ttk.Label(frm, text="Id блога"), blogid_entry],
    [ttk.Label(frm, text="Токен авторизации"), token_entry],
    [ttk.Button(frm, text="Загрузить блог в файл", command=lambda: blogToFile(blog_id, token))],
    [ttk.Button(frm, text="Импортировать файл тегов", command=lambda: (importTagsFileByBlogId(blog_id),
                                                                       startfileTagsFile(blog_id)))],
    [ttk.Button(frm, text="RestoreTS", command=lambda: (
        restoreTs(blog_id),
        startfileTagsFile(blog_id)
    ))],
    [ttk.Button(frm, text="merge", command=lambda: mergeMatrixPostsOnly(blog_id))],
    [ttk.Button(frm, text="Обновить теги матрицы по списку тегов", command=lambda: (
        updateTagMatrixTagsByBlogId(blog_id),
        startfileTagsFile(blog_id)
    ))],
    [ttk.Button(frm, text="Обновить посты матрицы из файла блога", command=lambda: updateMatrixPostsByBlogId(blog_id))],
    [ttk.Button(frm, text="Опубликовать новые теги из файла тегов", command=lambda: publish(blog_id, token))],
    [status_label]
]


def formatGrid():
    max_column_number = 0
    for row in children:
        row_len = len(row)
        if row_len > max_column_number:
            max_column_number = row_len

    for i in range(len(children)):
        for j in range(len(children[i])):
            children[i][j].grid(row=i, column=j, columnspan=int(max_column_number / len(children[i])), sticky="we"
                                , pady=2)
formatGrid()


root.mainloop()
