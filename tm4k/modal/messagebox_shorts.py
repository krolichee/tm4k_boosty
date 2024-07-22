from tkinter import messagebox


def ask(message:str)->str:
    return messagebox.askquestion("??",message , icon='warning')


def warn(message):
    messagebox.showwarning("!!", message)
