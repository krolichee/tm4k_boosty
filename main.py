import sys
import tkinter
import traceback

import tm4k_modal
# from pandas.io.excel._openpyxl import OpenpyxlWriter as OpenpyxlWriter


from tm4k_blog_parse import *
from tm4k_tags_wb_commands import *

import os.path
from tkinter import *
from tkinter import ttk

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def stuck():
    while True:
        pass


def suggestCreateTagsFile(blog_id: str):
    pass

def print_dataframe():
    openPostsList(blog_id)
    pass

#os.startfile("C:\\Users\\Puziko\\PycharmProjects\\TagMaster40000\\blogs\\marcykatya\\tags.xlsx")

#stuck()


blog_id = "marcykatya"
token = "8a5c35517e671a7cbdc9ebee526d758bad659ed0a53552b22a7c194cb8115946"

def setEntryText(entry:tkinter.Entry, text):
    entry.delete(0,tkinter.END)
    entry.insert(0, text)


def create_child_window():
    child_window = Toplevel(root)
    child_window.title("Дочернее окно")

    label = ttk.Label(child_window, text="Это дочернее окно")
    label.pack(padx=20, pady=20)

    close_button = ttk.Button(child_window, text="Закрыть", command=child_window.destroy)
    close_button.pack(pady=10)


root = Tk()
import tm4k_modal_root
tm4k_modal_root.root = root

frm = ttk.Frame(root, padding=10)
frm.grid()

blogid_entry = ttk.Entry(frm, validate="all")
setEntryText(blogid_entry, blog_id)
accept_blogid_button = ttk.Button(frm, text="Принять", command=lambda: setBlogId(blogid_entry.get()))

token_entry = ttk.Entry(frm, validate="all")
setEntryText(token_entry, token)
accept_token_button = ttk.Button(frm, text="Принять", command=lambda: setToken(token_entry.get()))

status_label = ttk.Label(frm,text="",foreground="dark gray")
import tm4k_status_label
tm4k_status_label.status_label = status_label



children = [
    [ttk.Label(frm, text="Id блога"), blogid_entry, accept_blogid_button],
    [ttk.Label(frm, text="Токен авторизации"), token_entry, accept_token_button],
    [ttk.Button(frm, text="Загрузить блог в файл", command=lambda: blogToFile(blog_id,token))],
    [ttk.Button(frm, text="Импортировать файл тегов", command=lambda: (importTagsFileByBlogId(blog_id),
                startfileTagsFile(blog_id)))],
    [ttk.Button(frm, text="RestoreTS",command=lambda:(
        restoreTs(blog_id),
        startfileTagsFile(blog_id)
    ))],
    [ttk.Button(frm, text="merge", command=lambda:mergeMatrixPostsOnly(blog_id))],
    [ttk.Button(frm, text="Обновить теги матрицы по списку тегов", command=lambda: (
        updateTagMatrixTagsByBlogId(blog_id),
        startfileTagsFile(blog_id)
    ))],
    [ttk.Button(frm, text="Обновить посты матрицы из файла блога", command=lambda: updateMatrixPostsByBlogId(blog_id))],
    [ttk.Button(frm, text="Опубликовать новые теги из файла тегов", command=lambda:publish(blog_id,token))],
    [status_label]
]

max_column_number = 0
for row in children:
    row_len = len(row)
    if row_len > max_column_number:
        max_column_number = row_len

for i in range(len(children)):
    for j in range(len(children[i])):
        children[i][j].grid(row=i, column=j, columnspan=int(max_column_number / len(children[i])), sticky="we",pady=2)

root.mainloop()

