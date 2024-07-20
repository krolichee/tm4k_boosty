import tkinter
from tkinter import *
from tkinter import ttk
from tm4k_modal_root import root
from tkinter import messagebox


def createChildWindow():
    child_window = Toplevel(root)
    child_window.title("Дочернее окно")

    label = ttk.Label(child_window, text="Это дочернее окно")
    label.pack(padx=20, pady=20)

    close_button = ttk.Button(child_window, text="Закрыть", command=child_window.destroy)
    close_button.pack(pady=10)