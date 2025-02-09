import os
from .blog_file import getBlogFolderDir
from pandas.io.excel._base import ExcelWriter as Writer
from typing import Literal

import tm4k.modal.messagebox_shorts as mb

from ..messages import NO_ACCES_TO_TAGS_FILE_MESSAGE


def getTagsFilePath(blog_id: str) -> str:
    return getBlogFolderDir(blog_id) + 'tags.xlsx'


def isTagsFileExists(blog_id: str) -> bool:
    return os.path.exists(getTagsFilePath(blog_id))


def getTagsFileWriter(blog_id: str, mode: Literal['w', 'a'],
                      if_sheet_exists: Literal["error", "new", "replace", "overlay"] = 'error') -> Writer:
    path = getTagsFilePath(blog_id)
    if mode != 'a':
        if_sheet_exists = None
    try:
        writer = Writer(path, engine='openpyxl', mode=mode, if_sheet_exists=if_sheet_exists)
    except PermissionError as err:
        print(err.filename)
        mb.warn(NO_ACCES_TO_TAGS_FILE_MESSAGE)
        raise err
    return writer
