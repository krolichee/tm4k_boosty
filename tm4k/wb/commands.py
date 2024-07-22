import pandas as pd
import numpy as np

import requests

from .format import *
from tm4k.messages import TAGS_FILE_ALLREADY_EXIST_QUESTION, NO_ACCES_TO_TAGS_FILE_MESSAGE

from ._names import *

from tm4k.fs.tags_file import *
from tm4k.fs.blog_file import *
from tm4k.post.edit_payload import getPostPayload

from tm4k.links import getPostApiLink, getPostLink
from tm4k.post.field import *


# todo обновление файла с сохранением цветов тегов, комментариев и т.п.

def createTagListDf(tag_list: list) -> pd.DataFrame:
    return pd.DataFrame({'Тег': tag_list, 'Комментарий': [None] * len(tag_list)})


def importTagsFileByBlogId(blog_id: str):
    posts_list = openBlogFile(blog_id)
    if posts_list is not None:
        importTagsFileFromBlog(posts_list)


def startfileTagsFile(blog_id: str):
    os.startfile(os.path.abspath(getTagsFilePath(blog_id)))


def importTagsFileFromBlog(posts_list: list):
    blog_id = getPostBlogId(posts_list[0])

    if checkTagsFileExists(blog_id):
        if mb.ask(TAGS_FILE_ALLREADY_EXIST_QUESTION) == 'no':
            return
    else:
        buildDirRecu(getTagsFilePath(blog_id))

    tag_list = getTagListFromBlog(posts_list)
    tag_list_df = createTagListDf(tag_list)
    tag_matrix_df = createTagMatrixDf(posts_list, tag_list)
    try:
        writer = getTagsFileWriter(blog_id, 'w')
    except:
        mb.warn(NO_ACCES_TO_TAGS_FILE_MESSAGE)
        return

    tag_matrix_df = fillDividerColumn(tag_matrix_df)

    tag_list_df.to_excel(writer, index=False, sheet_name=TAG_LIST_SHEET_NAME)
    tag_matrix_df.to_excel(writer, index=False, sheet_name=TAGS_MATRIX_SHEET_NAME)
    workbook = writer.book
    formatWorkbook(workbook)
    writer._save()


def fillDividerColumn(df: pd.DataFrame) -> pd.DataFrame:
    df[TMDS] = df[TMDS].fillna(TMDS)
    return df


def updateTagMatrixTagsByBlogId(blog_id: str):
    writer = getTagsFileWriter(blog_id, 'a', 'replace')
    workbook: Workbook = writer.book
    new_tag_matrix_df = getUpdatedTagMatrixDfFromWorkbook(workbook)
    new_tag_matrix_df = fillDividerColumn(new_tag_matrix_df)
    new_tag_matrix_df.to_excel(excel_writer=writer, sheet_name=TAGS_MATRIX_SHEET_NAME, index=False)
    formatWorkbook(workbook)
    writer._save()


def splitDfByHeader(df: pd.DataFrame, header: str, shift: int = 0) -> tuple[pd.DataFrame, pd.DataFrame]:
    right_index = list(df.keys()).index(header)
    return splitDfByColumnIndex(df, right_index, shift)


def getTagMatrixDfFromWorkbook(wb: Workbook):
    return getDfFromWorksheet(wb[TAGS_MATRIX_SHEET_NAME])


def getTagListDfFromWorkbook(wb: Workbook):
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
    print(df)
    for col in df.columns:
        df[col] = np.where(df[col].isna(), pd.NA, col)
        df[str(col)] = df[str(col)].apply(lambda x: col if True else pd.NA)
        df[col] = df[col].apply(lambda x: pd.NA if pd.isna(x) else col)
    return df


def splitDfByDividerColumn(df: pd.DataFrame, column_name: str):
    df1, df2_div = splitDfByHeader(df, column_name)
    div_df, df2 = splitDfByHeader(df2_div, column_name, +1)
    return df1, df2, div_df


def getUpdatedTagMatrixDfFromWorkbook(wb: Workbook):
    # TODO обработка повторяющихся столбцов
    tag_list = getTagListFromWorkbook(wb)
    tag_matrix_df = getTagMatrixDfFromWorkbook(wb)
    df1, raw_matrix_df, div_df = splitDfByDividerColumn(tag_matrix_df, TAGS_MATRIX_DIVIDER_SYMBOL)
    sorted_raw_matrix_df = addAndSortByHeaderList(raw_matrix_df, tag_list)
    repl_sorted_raw_matrix_df = replaceNotNullCellsToColumnHeaderDf(sorted_raw_matrix_df)
    new_tag_matrix_df = pd.concat([df1, div_df, repl_sorted_raw_matrix_df], axis=1)
    return new_tag_matrix_df


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
    tags_df = getTagListDfFromWorkbook(wb)
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


def merge(blog_id):
    writer = getTagsFileWriter(blog_id, mode='a', if_sheet_exists='replace')
    wb = writer.book
    m_df_a = getDfFromWorksheet(wb["Матрица тегов A"])
    m_df_b = getDfFromWorksheet(wb["Матрица тегов B"])
    unique_values_list_a = m_df_a.loc[~m_df_a['ID'].isin(m_df_b['ID']), 'ID'].tolist()
    unique_values_list_b = m_df_b.loc[~m_df_b['ID'].isin(m_df_a['ID']), 'ID'].tolist()
    merged = m_df_a.merge(m_df_b, how='right', left_on=["ID"], right_on=["ID"])
    # sorted_merged = merged.sort_values(by="TS")

    merged.to_excel(writer, "Матрица тегов Merged", index=False)
    formatWorkbook(wb)
    writer._save()
    print(unique_values_list_a)
    print(unique_values_list_b)


def updateMatrixPostsByBlogId(blog_id: str):
    writer = getTagsFileWriter(blog_id, 'a')
    wb = writer.book
    matrix_df = getTagMatrixDfFromWorkbook(wb)
    posts_list = openBlogFile(blog_id)
    matrix_df_id_list = list(matrix_df["ID"])
    new_ids = []
    for post in posts_list:
        post_id = getPostId(post)
        if post_id not in matrix_df_id_list:
            post_df = getPostDf(post)
            matrix_df = pd.concat([matrix_df, post_df], ignore_index=True, axis='rows')
            new_ids.append(post_id)
    matrix_df = matrix_df.sort_values(by='TS', ascending=False)
    matrix_df.to_excel(writer, "updateMatrixPostsByBlogId", index=False)
    wb = writer.book
    highlightRowWhereIn(wb["updateMatrixPostsByBlogId"], "ID", new_ids)
    writer._save()


def restoreTs(blog_id):
    posts_list = openBlogFile(blog_id)
    post_id_ts_list = {'ID': [],
                       'TS': []}
    for post in posts_list:
        post_id = getPostId(post)
        post_id_ts_list['ID'].append(post_id)
        ts = getPostPublishTs(post)
        post_id_ts_list['TS'].append(ts)
    writer = getTagsFileWriter(blog_id, mode='a', if_sheet_exists='replace')
    wb = writer.book
    no_ts_ws = wb[TAGS_MATRIX_SHEET_NAME]
    no_ts_df = getDfFromWorksheet(no_ts_ws)
    post_ids_df = pd.DataFrame(post_id_ts_list)
    restored_df = no_ts_df.merge(post_ids_df, how="left", on="ID")

    missing_ts_mask = restored_df['TS'].isna()
    restored_df.loc[missing_ts_mask, 'TS'] = restored_df.loc[missing_ts_mask, 'ID'].apply(lambda x: getPostPublishTs(
        requests.get(
            getPostApiLink(blog_id, x))
        .json()))
    restored_df = sortDfByHeaderList(restored_df, TAGS_MATRIX_DF_COLS_LIST)
    restored_df = restored_df.sort_values(by='TS', ascending=False)
    restored_df.to_excel(writer, "Матрица тегов Restored TS", index=False)
    writer._save()


def normalizeAndFormatTagsFile(blog_id):
    writer = getTagsFileWriter(blog_id, 'a', 'replace')
    wb: Workbook = writer.book
    ws: Worksheet = wb[TAGS_MATRIX_SHEET_NAME]
    df = getDfFromWorksheet(ws)
    df = replaceNotNullCellsToColumnHeaderDf(df)
    df.to_excel(writer, TAGS_MATRIX_SHEET_NAME, index=False)
    formatWorkbook(wb)
    writer._save()


def publish(blog_id: str, token: str):
    normalizeAndFormatTagsFile(blog_id)
    writer = getTagsFileWriter(blog_id, 'a')
    wb: Workbook = writer.book
    ws = wb[TAGS_MATRIX_SHEET_NAME]
    df = getDfFromWorksheet(ws)
    headers = {'Authorization': f'Bearer {token}'}
    posts_list = openBlogFile(blog_id)
    for post in posts_list:
        post_id = getPostId(post)
        row_df = df.loc[df['ID'] == getPostId(post)]
        tag_list = []
        _, tags_df = splitDfByHeader(row_df, TAGS_MATRIX_DIVIDER_SYMBOL, +1)
        for tag_cell in tags_df.iloc[0]:
            print(tag_cell)
            if tag_cell is not None:
                tag_list.append(tag_cell)

        payload = getPostPayload(post)

        payload['tags'] = ",".join(tag_list)

        url = getPostApiLink(blog_id, post_id)

        response = requests.put(url, data=payload, headers=headers)
        print(response)
        print(response.text)


def getTagListFromBlog(posts_list):
    tag_list = []
    for post in posts_list:
        for tag_obj in post["tags"]:
            tag = tag_obj["title"]
            if tag not in tag_list:
                tag_list.append(tag)
    return tag_list
