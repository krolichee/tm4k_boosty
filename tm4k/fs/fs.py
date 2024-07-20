import os


def getCreateMethod(path):
    return "w" if os.path.isfile(path) else "x"


def mkdirIfNotExist(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)
