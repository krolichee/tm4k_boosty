import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from tm4k.fs import getTagsFileWriter
from tm4k.links import getPostLink
from tm4k.post.field import getSubscrLvlName, getPostId, getPostPublishTs
from pandas.io.excel._base import ExcelWriter as Writer

from tm4k.wb._names import TMDS, TAGS_MATRIX_SHEET_NAME, TAG_LIST_SHEET_NAME, TAGS_MATRIX_DIVIDER_SYMBOL, \
    TAGS_MATRIX_DF_COLS_LIST


def fillDividerColumn(df: pd.DataFrame) -> pd.DataFrame:
    df[TMDS] = df[TMDS].fillna(TMDS)
    return df


def splitDfByHeader(df: pd.DataFrame, header: str, shift: int = 0) -> tuple[pd.DataFrame, pd.DataFrame]:
    right_index = list(df.keys()).index(header)
    return splitDfByColumnIndex(df, right_index, shift)


def getTagMatrixDf(wb: Workbook):
    return getDfFromWorksheet(wb[TAGS_MATRIX_SHEET_NAME])


def getTagListDf(wb: Workbook):
    return getDfFromWorksheet(wb[TAG_LIST_SHEET_NAME])


def splitDfByColumnIndex(df: pd.DataFrame, index: int, shift: int = 0) -> tuple[pd.DataFrame, pd.DataFrame]:
    df1 = df.iloc[:, :(index + shift)]
    df2 = df.iloc[:, (index + shift):]
    return df1, df2


def makeDfByHeaderListAndLength(header_list: list, length: int):
    data = {}
    for header in header_list:
        data[header] = [None] * length
    return pd.DataFrame(data)


def addMissingHeaders(df: pd.DataFrame, header_list: list) -> pd.DataFrame:
    for header in header_list:
        if header not in df.columns:
            df[header] = pd.NA
    return df


def sortDfByHeaderList(df: pd.DataFrame, header_list: list) -> pd.DataFrame:
    all_cols = list(df.keys())
    remaining_cols = [col for col in all_cols if col not in header_list]
    final_order = header_list + remaining_cols
    return df[final_order]


def addAndSortByHeaderList(df: pd.DataFrame, header_list: list):
    df = addMissingHeaders(df, header_list)
    return sortDfByHeaderList(df, header_list)


def replaceNotNullCellsToColumnHeaderDf(df: pd.DataFrame):
    for col in df.columns:
        df[col] = np.where(df[col].isna(), pd.NA, col)
        df[str(col)] = df[str(col)].apply(lambda x: col if True else pd.NA)
        df[col] = df[col].apply(lambda x: pd.NA if pd.isna(x) else col)
    return df


def splitDfByDividerColumn(df: pd.DataFrame, column_name: str):
    """

    :param df:
    :param column_name:
    :return: left Df, div Df, right Df
    """
    df1, df2_div = splitDfByHeader(df, column_name)
    div_df, df2 = splitDfByHeader(df2_div, column_name, +1)
    return df1, div_df, df2


def reviseTagMatrixInWb(writer: Writer):
    wb: Workbook = writer.book
    tag_list = getTagListFromWorkbook(wb)
    tag_matrix_df = getTagMatrixDf(wb)
    df1, div_df, rawm_df = splitDfByDividerColumn(tag_matrix_df, TAGS_MATRIX_DIVIDER_SYMBOL)
    print('Разделенная матрица: ')
    print(df1)
    print(div_df)
    print(rawm_df)
    added_rawm_df = addMissingHeaders(rawm_df, tag_list)
    sorted_rawm_df = sortDfByHeaderList(added_rawm_df, tag_list)
    repl_rawm_df = replaceNotNullCellsToColumnHeaderDf(sorted_rawm_df)
    div_df = fillDividerColumn(div_df)
    print('Переработанная матрица: ')
    print(df1)
    print(div_df)
    print(rawm_df)
    new_tag_matrix_df = pd.concat([df1, div_df, repl_rawm_df], axis=1)
    new_tag_matrix_df.to_excel(writer, index=False, sheet_name=TAGS_MATRIX_SHEET_NAME)



def getPostDict(post: dict):
    result = {"Название": post["title"],
              "Уровень подписки": getSubscrLvlName(post),
              "ID": getPostId(post),
              "TS": getPostPublishTs(post),
              "Ссылка": getPostLink(post)
              }
    for tag_obj in post["tags"]:
        tag = tag_obj["title"]
        result[tag] = tag
    return result


def getPostDf(post):
    post_row_dict = getPostDict(post)
    post_df = pd.DataFrame(post_row_dict, index=[0])
    return post_df


def createTagMatrixDf(posts_list: list, tag_list: list):
    df = pd.DataFrame(columns=TAGS_MATRIX_DF_COLS_LIST + [TAGS_MATRIX_DIVIDER_SYMBOL] + tag_list)
    for post in posts_list:
        post_df = getPostDf(post)
        df = pd.concat([df, post_df], ignore_index=True)
    return df


def getDfFromWorksheet(ws: Worksheet):
    data = ws.values
    columns = [str(x) for x in next(data)]
    df = pd.DataFrame(data, columns=columns)
    return df


def getTagListFromWorkbook(wb: Workbook) -> list:
    tags_df = getTagListDf(wb)
    tag_list = [tag for tag in list(tags_df["Тег"]) if tag is not None]
    return tag_list


def mergeMatrixPostsOnly(blog_id):
    writer = getTagsFileWriter(blog_id, mode='a', if_sheet_exists='replace')
    wb = writer.book
    m_df_a = getDfFromWorksheet(wb["Матрица тегов A"])
    m_df_b = getDfFromWorksheet(wb["Матрица тегов B"])
    print(m_df_b[TAGS_MATRIX_DF_COLS_LIST])
    print(m_df_b.loc[~m_df_b['ID'].isin(m_df_a['ID']), 'ID'])

    unique_values_list_b = m_df_b.loc[~m_df_b['ID'].isin(m_df_a['ID']), 'ID'].tolist()


def getTagListFromBlog(posts_list):
    tag_list = []
    for post in posts_list:
        for tag_obj in post["tags"]:
            tag = tag_obj["title"]
            if tag not in tag_list:
                tag_list.append(tag)
    return tag_list
