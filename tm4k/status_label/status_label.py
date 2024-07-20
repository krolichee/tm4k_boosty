from .config import *


def updateStatus(message: str):
    status_label = getLabel()
    print("status: ", message)
    status_label.config(text=message)
    status_label.update_idletasks()
