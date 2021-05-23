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


def select_u(user_id, *args):
    """
    查询"u"表中的数据,调用select_base接口
    :param user_id: 被查询的用户id
    :param args: 所有被查询的字段名
    :return:
    """
    return select_base('u', *args, id=user_id)


def update_u(user_id, kwargs):
    """
    更新"u"表中的数据,调用update_base接口
    :param user_id:
    :param kwargs: 需要更改的数据dict,{需要更改的字段名:更改之后的值,...}
    :return:
    """
    update_base('u', {'id': user_id}, **kwargs)


def insert_u(user_id):
    """
    注册u表
    :param user_id:
    :return:
    """
    insert_base('u', user_id)


def select_wx(user_id, *args):
    """
    查询"wx"表中的数据,调用select_base接口
    :param user_id: 被查询的用户id
    :param args: 所有被查询的字段名
    :return:
    """
    return select_base('wx', *args, id=user_id)


def select_any_in_wx(where_dict, *args):
    """
    查询"wx"表中的数据,调用select_base接口, 不以user_id为查询
    :param where_dict: 查询条件dict,{字段名：值}
    :param kwargs: 需要更改的数据dict,{需要更改的字段名:更改之后的值,...}
    :return:
    """
    return select_base('wx', *args, **where_dict)


def update_wx(user_id, kwargs):
    """
    更新"wx"表中的数据,调用update_base接口
    :param user_id:
    :param kwargs: 需要更改的数据dict,{需要更改的字段名:更改之后的值,...}
    :return:
    """
    update_base('wx', {'id': user_id}, **kwargs)


def insert_wx(user_id):
    """
    注册wx表
    :param user_id:
    :return:
    """
    insert_base('wx', user_id)


def select_card(user_id, *args):
    """
    查询"card"表中的数据,调用select_base接口
    :param user_id: 被查询的用户id
    :param args: 所有被查询的字段名
    :return:
    """
    return select_base('card', *args, id=user_id)


def update_card(where_dict, kwargs):
    """
    更新"card"表中的数据,调用update_base接口
    :param where_dict: 查询条件dict,{字段名：值}
    :param kwargs: 需要更改的数据dict,{需要更改的字段名:更改之后的值,...}
    :return:
    """
    update_base('card', where_dict, **kwargs)


def insert_card(user_id):
    """
    注册card表
    :param user_id:
    :return:
    """
    insert_base('card', user_id)


def select_game(user_id, *args):
    """
    查询"game"表中的数据,调用select_base接口
    :param user_id: 被查询的用户id
    :param args: 所有被查询的字段名
    :return:
    """
    return select_base('game', *args, id=user_id)


def update_game(user_id, kwargs):
    """
    更新"game"表中的数据,调用update_base接口
    :param user_id:
    :param kwargs: 需要更改的数据dict,{需要更改的字段名:更改之后的值,...}
    :return:
    """
    update_base('game', {'id': user_id}, **kwargs)


def insert_game(user_id):
    """
    插入游戏用户信息
    :param user_id:
    :return:
    """
    insert_base('game', user_id)


def select_bank(user_id, *args):
    """
    查询"bank"表中的数据,调用select_base接口
    :param user_id: 被查询的用户id
    :param args: 所有被查询的字段名
    :return:
    """
    return select_base('bank', *args, id=user_id)


def update_bank(user_id, kwargs):
    """
    更新"bank"表中的数据,调用update_base接口
    :param user_id:
    :param kwargs: 需要更改的数据dict,{需要更改的字段名:更改之后的值,...}
    :return:
    """
    update_base('bank', {'id': user_id}, **kwargs)


def insert_bank(user_id):
    """
    注册bank表信息
    :param user_id:
    :return:
    """
    insert_base('bank', user_id)


def insert_base(base, user_id):
    """
    增加数据
    :param base:
    :param user_id:
    :return:
    """
    con, cur = get_cur()
    sql = f'insert into {base}(Id) value({user_id})'
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()


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
        where_str = f'{_}="{kwargs[_]}"'
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
