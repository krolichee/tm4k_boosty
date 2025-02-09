import tkinter as tk
from tkinter import *
from tkinter import ttk
from .config import *
from tkinter import messagebox


__all__ = ['showMultipleChoiceModal']
def showMultipleChoiceModal(title:str,options:list[str]):
    root = getRoot()
    child_window = Toplevel(root)
    child_window.title(title)
    child_window.grab_set()
    child_window.geometry("250x130")
    child_window.config(pady=10)
    cb_conf = []
    for opt in options:
        cb_conf.append({'text':opt, 'variable':tk.BooleanVar(value=True)})
    cb_list = []
    for i in cb_conf:
        i.update({'master': child_window})
        i['variable'].set(True)
        cb = ttk.Checkbutton(**i)
        cb.pack(anchor='w', padx=10)
        cb_list.append(cb)
    ttk.Button(child_window, text="ОК",command=child_window.destroy).pack(anchor='s', pady=10)
    root.wait_window(child_window)
    result = [x['variable'].get() for x in cb_conf]
    return result


def createChildWindow():
    child_window = Toplevel(getRoot())
    child_window.title("Дочернее окно")
    label = ttk.Label(child_window, text="Это дочернее окно")
    label.pack(padx=20, pady=20)
    close_button = ttk.Button(child_window, text="Закрыть", command=child_window.destroy)
    close_button.pack(pady=10)
