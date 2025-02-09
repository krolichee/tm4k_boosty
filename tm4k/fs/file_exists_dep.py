""
import os
from functools import wraps
from typing import Callable

# ssk - path:str # ssv - {'op': foo(ctr,fl:bool),'dpnds':Any}

sss = {}


def updateDeps():
    for ssk, ssv in sss.items():
        for s in ssv['dpnds']:
            ssv['op'](s, os.path.isfile(ssk))


def newPath(path: str, op: Callable):
    sss[path] = {'op': op, 'dpnds': []}


def newDep(path: str, obj):
    sss[path]['dpnds'].append(obj)
    updateDeps()

def updating_fe_dep(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        result = func(*args,**kwargs)
        updateDeps()
        return result
    return wrapper
