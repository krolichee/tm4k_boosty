import os


def getCreateMethod(path):
    return "w" if os.path.isfile(path) else "x"

def buildDirRecu(path:str):
    path_parts = path.split('/')
    temp_path = ""
    for part in path_parts[:-1]:
        temp_path += f"{part}/"
        mkdirIfNotExist(temp_path)
        print(temp_path)

def mkdirIfNotExist(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)
