from enum import Enum

from .config import *

__all__ = ['updateStatus', 'setStatusLabel']


def getPref():
    pass


cf = {
    'err': {
        'foreground': '#FF5555'
    },
    'warn': {
        'foreground': '#FFFF55'
    },
    "com": {
        'foreground': 'dark gray'
    }
}

Status = Enum('Satus', list(cf.keys()))


def processPrefixedMessage(pref: Status):
    result = {}
    result.update(cf[pref])
    return result


def updateStatus(message: str, pref: Status = 'com'):
    print(message)
    status_label = getLabel()
    label_cfg = {'text': message}
    label_cfg.update(processPrefixedMessage(pref))
    status_label.config(**label_cfg)
    status_label.update_idletasks()

