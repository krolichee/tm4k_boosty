from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
from ._names import TAG_LIST_SHEET_NAME, TAGS_MATRIX_SHEET_NAME


def isTagListSheetExist(wb: Workbook):
    return isSheetExists(wb, TAG_LIST_SHEET_NAME)


def isTagMatrixSheetExist(wb: Workbook):
    return isSheetExists(wb, TAGS_MATRIX_SHEET_NAME)


def isSheetExists(wb: Workbook, name: str) -> bool:
    try:
        _ = wb[name]
        return True
    except:
        return False
