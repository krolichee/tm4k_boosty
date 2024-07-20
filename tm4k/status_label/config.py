import tkinter.ttk as ttk

__all__ = ['setLabel', 'getLabel']

_status_label: ttk.Label = None


def setLabel(label: ttk.Label):
    global _status_label
    _status_label = label


def getLabel():
    return _status_label
