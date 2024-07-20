import os
from blog_file import getBlogFolderPath
from pandas.io.excel._base import ExcelWriter as Writer
from typing import Literal


def getTagsFilePath(blog_id: str) -> str:
    return getBlogFolderPath(blog_id) + 'tags.xlsx'


def checkTagsFileExists(blog_id: str) -> bool:
    return os.path.exists(getTagsFilePath(blog_id))


def getTagsFileWriter(blog_id: str, mode: Literal['w', 'a'],
                      if_sheet_exists: Literal["error", "new", "replace", "overlay"] = 'error') -> Writer:
    path = getTagsFilePath(blog_id)
    if mode != 'a':
        if_sheet_exists = None
    writer = Writer(path, engine='openpyxl', mode=mode, if_sheet_exists=if_sheet_exists)
    return writer
