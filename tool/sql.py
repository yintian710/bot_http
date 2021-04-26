# -*- coding: utf-8 -*-
"""
@File  : sql.py
@Author: yintian
@Date  : 2021/3/31 15:24
@Desc  : 
"""
import json

import pymysql

from tool.CONTANT import SQL_PATH

with open(SQL_PATH, 'r', encoding="utf-8") as f:
    sql_json = json.loads(f.read())


def get_cur():
    con = pymysql.connect(**sql_json)
    return con, con.cursor()


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
    return select_base('u', *args, id=user_id)


def update_u_for_sql(user_id, kwargs):
    update_base('u', {'id': user_id}, **kwargs)


def select_card_for_sql(user_id, *args):
    return select_base('card', *args, id=user_id)


def update_card_for_sql(where_dict, kwargs):
    update_base('card', where_dict, **kwargs)


def select_base(base, *args, **kwargs):
    con, cur = get_cur()
    where_str = ''
    for _ in kwargs:
        where_str = f'{_}={kwargs[_]}'
    sql = f'select {",".join(args)} from {base}'
    if where_str:
        sql += f' where {where_str}'
    res = cur.execute(sql)
    result = False
    if res:
        result = cur.fetchone()
    cur.close()
    con.close()
    return result


def update_base(base, where_dict, **kwargs):
    con, cur = get_cur()
    update_str = ''
    sql = f'update {base} set '
    where_str = ''
    if not where_dict and where_dict != 0:
        return '请添加限制条件'
    for _ in kwargs:
        update_str += f'{_}="{kwargs[_]}",'
    if not update_str:
        return f'更改{kwargs}失败'
    sql += update_str[:-1]
    for _ in where_dict:
        where_str = f'{_}={where_dict[_]}'
    if where_str:
        sql += f' where {where_str}'
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

if __name__ == '__main__':
    print()