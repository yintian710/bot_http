# -*- coding: utf-8 -*-
"""
@File  : sql.py
@Author: yintian
@Date  : 2021/3/31 15:24
@Desc  : sql代码模块,被所有业务调用
"""
import json

import pymysql

from tool.CONTANT import SQL_PATH

# 读取sql.json文件,获取mysql连接账号密码
with open(SQL_PATH, 'r', encoding="utf-8") as f:
    sql_json = json.loads(f.read())


def get_cur():
    """
    获取mysql连接,并返回两个操作参数
    :return:
    """
    con = pymysql.connect(**sql_json)
    cur = con.cursor()
    return con, cur


# def select_u(user_id, *args):
#     con, cur = get_cur()
#     sql = f'select {",".join(args)} from u where id={user_id}'
#     res = cur.execute(sql)
#     if res:
#         result = cur.fetchone()
#         return result
#     return False


# def update_u_for_sql(user_id, **kwargs):
#     con, cur = get_cur()
#     update_str = ''
#     for _ in kwargs:
#         update_str += f'{_}="{kwargs[_]}",'
#     sql = f'update u set {update_str[:-1]} where id={user_id}'
#     cur.execute(sql)
#     con.commit()
#     cur.close()
#     con.close()


def select_u_for_sql(user_id, *args):
    """
    查询"u"表中的数据,调用select_base接口
    :param user_id: 被查询的用户id
    :param args: 所有被查询的字段名
    :return:
    """
    return select_base('u', *args, id=user_id)


def update_u_for_sql(user_id, kwargs):
    """
    更新"u"表中的数据,调用update_base接口
    :param user_id:
    :param kwargs: 需要更改的数据dict,{需要更改的字段名:更改之后的值,...}
    :return:
    """
    update_base('u', {'id': user_id}, **kwargs)


def select_card_for_sql(user_id, *args):
    """
    查询"card"表中的数据,调用select_base接口
    :param user_id: 被查询的用户id
    :param args: 所有被查询的字段名
    :return:
    """
    return select_base('card', *args, id=user_id)


def update_card_for_sql(where_dict, kwargs):
    """
    更新"card"表中的数据,调用update_base接口
    :param where_dict: 查询条件dict,{字段名：值}
    :param kwargs: 需要更改的数据dict,{需要更改的字段名:更改之后的值,...}
    :return:
    """
    update_base('card', where_dict, **kwargs)


def select_base(base, *args, **kwargs):
    """
    查询数据库底层接口
    :param base: 查询的表的名称
    :param args: 需要查询的字段名
    :param kwargs: 查询条件
    :return:
    """
    con, cur = get_cur()
    where_str = ''
    for _ in kwargs:
        where_str = f'{_}={kwargs[_]}'
    sql = f'select {",".join(args)} from {base}'
    if where_str:
        sql += f' where {where_str}'
    # sql: select score, N, SR from u where id=1327960105
    res = cur.execute(sql)
    result = False
    if res:
        result = cur.fetchone()
    cur.close()
    con.close()
    return result


def update_base(base, where_dict, **kwargs):
    """
    更改数据库底层接口
    :param base: 更改的表的名称
    :param where_dict: 需要更改的字段数据dict,{需要更改的字段名:更改之后的值,...}
    :param kwargs: 查询条件
    :return:
    """
    con, cur = get_cur()
    update_str = ''
    sql = f'update {base} set '
    where_str = ''
    if not where_dict and where_dict != 0:
        return '请添加限制条件'
    for _ in kwargs:
        update_str += f'{_}="{kwargs[_]}",'
    # sql: update u set score="100", da="2021-04-30",
    if not update_str:
        return f'更改{kwargs}失败'
    sql += update_str[:-1]
    # sql: update u set score="100", da="2021-04-30"
    if where_dict != 0:
        for _ in where_dict:
            where_str = f'{_}={where_dict[_]}'
        if where_str:
            sql += f' where {where_str}'
        # sql: sql: update u set score="100", da="2021-04-30" where id=1327960105
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()
