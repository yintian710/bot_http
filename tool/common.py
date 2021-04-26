# -*- coding: utf-8 -*-
"""
@File  : common.py
@Author: yintian
@Date  : 2021/3/31 15:40
@Desc  : 
"""

import json
import re

from tool.sql import select_u_for_sql, update_u_for_sql


def get_return(message, code=0):
    return json.dumps({'code': code, 'message': message})


def is_regis(func):
    def inner(user_id, *args, **kwargs):
        if not select_u_for_sql(user_id, 'id'):
            return get_return('您还没有注册，请先注册', 1)
        return func(user_id, *args, **kwargs)
    return inner


def is_admin(func):
    def inner(user_id, *args, **kwargs):
        permission = select_u_for_sql(user_id, 'permission')
        if not permission or permission != ('admin',):
            return get_return('爬', 1)
        return func(user_id, *args, **kwargs)

    return inner


def str_to_python_code(_str1):
    try:
        if 'time.sleep' in _str1:
            return 'sleep方法暂不支持。'
        _str1 = 'str1=""' + re.sub('print\(', 'str1 += f"\\\\n" + str(', _str1)
        print(_str1)
        write = '\nwith open("str.txt", "w", encoding="utf-8"' + ') as f:\n f.write(str(str1))'
        exec(_str1 + write)
        with open("str.txt", "r", encoding="utf-8") as f:
            str1 = f.read()
        # os.remove("str.txt")
        return str1
    except Exception as e:
        return e


def select_score(user_id):
    score = select_u_for_sql(user_id, 'score')[0]
    return score


def change_score(user_id, score, today):
    if score < 0:
        score = 0
    update_u_for_sql(user_id, {'score': score, 'da':today})


def add_score(user_id, new_score):
    old_score = select_score(user_id)
    if new_score + old_score < 0:
        new_score = 0
    else:
        new_score += old_score
    update_u_for_sql(user_id, {"score":new_score})


def enough_score(user_id, score):
    score1 = select_score(user_id)
    if score1 >= score:
        return score1
    return False


if __name__ == '__main__':
    str1 = """print(136845)"""
    a = str_to_python_code(str1)
    print(a)
