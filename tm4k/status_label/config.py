import tkinter.ttk as ttk

__all__ = ['setStatusLabel', 'getLabel']

_status_label: ttk.Label = None


def setStatusLabel(label: ttk.Label):
    global _status_label
    _status_label = label


def getLabel():
    return _status_label
