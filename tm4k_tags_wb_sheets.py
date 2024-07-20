from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
from tm4k_sheet_names import *


def isTagListSheetExist(wb: Workbook):
    isSheetExists(wb, TAG_LIST_SHEET_NAME)
    pass


def isSheetExists(wb: Workbook, name: str) -> bool:
    try:
        wb[name]
        return True
    except:
        return False
