from functools import wraps

import pandas as pd

import requests

import tm4k.modal

from .df_utils import *

from .format import *

from ._names import *

from tm4k.fs.tags_file import *
from tm4k.fs.blog_file import *
from tm4k.post.edit_payload import getPostPayload

from tm4k.links import getPostApiLink
from tm4k.post.field import *

from tm4k.modal import *

from tm4k.fs import openBlogFile, isBlogFileExists, saveBlog
from tm4k.messages import BLOG_FILE_NOT_EXIST_MESSAGE, BLOG_FILE_EXISTS_REWRITE_QUESTION
from tm4k.parse import parseBlog
from tm4k.post.field import getPostPublishTs
from tm4k.status_label import updateStatus


# todo обновление файла с сохранением цветов тегов, комментариев и т.п.


def startfile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        blog_id = kwargs.get('blog_id')
        if blog_id is not None:
            startfileTagsFile(blog_id)
        return result

    return wrapper


@startfile
def importTagsFileByBlogId(blog_id: str):
    blog = openBlogFile(blog_id)
    if len(blog):
        importTagsFileFromBlog(blog)


def createTagListDf(tag_list: list) -> pd.DataFrame:
    return pd.DataFrame({'Тег': tag_list, 'Комментарий': [None] * len(tag_list)})


def startfileTagsFile(blog_id: str):
    os.startfile(os.path.abspath(getTagsFilePath(blog_id)))


def importTagsFileFromBlog(posts_list: list):
    blog_id = getPostBlogId(posts_list[0])
    if isTagsFileExists(blog_id):
        if mb.ask(TAGS_FILE_ALLREADY_EXIST_QUESTION) == 'no':
            return
    else:
        buildDirRecu(getTagsFilePath(blog_id))
    tag_list = getTagListFromBlog(posts_list)
    tag_list_df = createTagListDf(tag_list)
    tag_matrix_df = createTagMatrixDf(posts_list, tag_list)
    writer = getTagsFileWriter(blog_id, 'w')
    tag_matrix_df = fillDividerColumn(tag_matrix_df)
    tag_list_df.to_excel(writer, index=False, sheet_name=TAG_LIST_SHEET_NAME)
    tag_matrix_df.to_excel(writer, index=False, sheet_name=TAGS_MATRIX_SHEET_NAME)
    workbook = writer.book
    formatWorkbook(workbook)
    writer._save()
    updateStatus("Тегфайл создан")


def refreshTagMatrixTags(blog_id: str):
    # fixme почему-то заполнение всех ячеек тегов
    writer = getTagsFileWriter(blog_id, 'a', 'replace')
    wb: Workbook = writer.book
    reviseTagMatrixInWb(writer)
    tag_matrix_df = getTagMatrixDf(wb)
    print(tag_matrix_df)
    tag_matrix_df.to_excel(excel_writer=writer, sheet_name=TAGS_MATRIX_SHEET_NAME, index=False)
    wb: Workbook = writer.book
    formatWorkbook(wb)
    writer._save()


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


def updateMatrixDfWithBlog(df: pd.DataFrame, blog: Blog):
    new_ids = []
    matrix_df_id_list = list(df["ID"])
    for post in blog:
        post_id = getPostId(post)
        if post_id not in matrix_df_id_list:
            post_df = getPostDf(post)
            df = pd.concat([df, post_df], ignore_index=True, axis='rows')
            new_ids.append(post_id)
    return df, new_ids


def updateMatrixPostsByBlogId(blog_id: str):
    writer = getTagsFileWriter(blog_id, 'a',if_sheet_exists='replace')
    wb = writer.book
    blog = openBlogFile(blog_id)
    matrix_df = getTagMatrixDf(wb)

    matrix_df,new_ids = updateMatrixDfWithBlog(matrix_df, blog)
    matrix_df = matrix_df.sort_values(by='TS', ascending=False)
    matrix_df.to_excel(writer, TAGS_MATRIX_SHEET_NAME, index=False)

    wb = writer.book
    highlightRowWhereIn(wb[TAGS_MATRIX_SHEET_NAME], "ID", new_ids)
    writer._save()


def getIdTsDfFromBlog(blog: Blog):
    post_id_ts_list = {'ID': [], 'TS': []}
    for post in blog:
        post_id = getPostId(post)
        ts = getPostPublishTs(post)
        post_id_ts_list['ID'].append(post_id)
        post_id_ts_list['TS'].append(ts)
    return pd.DataFrame(post_id_ts_list)


def restoreTs(blog_id):
    blog = openBlogFile(blog_id)
    writer = getTagsFileWriter(blog_id, mode='a', if_sheet_exists='replace')
    wb = writer.book
    no_ts_ws = wb[TAGS_MATRIX_SHEET_NAME]
    no_ts_df = getDfFromWorksheet(no_ts_ws)
    post_ids_df = getIdTsDfFromBlog(blog)
    restored_df = no_ts_df.merge(post_ids_df, how="left", on="ID")
    restored_df = sortDfByHeaderList(restored_df, TAGS_MATRIX_DF_COLS_LIST)
    restored_df = restored_df.sort_values(by='TS', ascending=False)
    restored_df.to_excel(writer, "Матрица тегов Restored TS", index=False)
    writer._save()


def refreshTagFile(blog_id):
    choice_dict = {"Обновить посты": updateMatrixPostsByBlogId,
                   "Обновить поля тегов": refreshTagMatrixTags,
                   "Обновить форматирование": normalizeAndFormatTagsFile}
    choice = showMultipleChoiceModal("Обноление файла тегов", list(choice_dict.keys()))
    for i in range(len(choice)):
        if choice[i]:
            list(choice_dict.values())[i](blog_id)


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


def updateBlog(blog_id: str, token: str):
    cur_blog = openBlogFile(blog_id)
    if not cur_blog:
        return
    last_post = cur_blog[0]
    from_ts = getPostPublishTs(last_post) + 1
    new_posts_blog = parseBlog(blog_id, token, from_ts)
    updated_blog = new_posts_blog + cur_blog
    return updated_blog


def refreshBlogFile(blog_id: str, token: str):
    if not isBlogFileExists(blog_id):
        updateStatus(BLOG_FILE_NOT_EXIST_MESSAGE)
        parseBlogToFile(blog_id, token)
        return
    updated_blog = updateBlog(blog_id, token)
    saveBlog(updated_blog)


def parseBlogToFile(blog_id: str, token: str):
    if isBlogFileExists(blog_id):
        if not mb.ask(BLOG_FILE_EXISTS_REWRITE_QUESTION) == 'yes':
            return
    updateStatus("Начало загрузки блога...")
    blog = parseBlog(blog_id, token)
    saveBlog(blog)
