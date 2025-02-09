from tkinter import messagebox


def ask(message:str)->str:
    return messagebox.askquestion("??",message , icon='warning')


def warn(message):
    messagebox.showwarning("!!", message)


def err(message):
    messagebox.showerror("XX",message)


def unexp():
    err("Произошло нечто неожиданное")