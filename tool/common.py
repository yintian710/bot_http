# -*- coding: utf-8 -*-
"""
@File  : common.py
@Author: yintian
@Date  : 2021/3/31 15:40
@Desc  : 公共方法模块
"""
import datetime
import json
import re

from tool.sql import select_u_for_sql, update_u_for_sql


def get_return(public_msg, private_msg='', public_id=0, private_id=0, need=None, code=0):
    """
    获取一个符合flask返回格式的dict
    :param need: 需要额外发送的数据
    :param private_id: 发送私聊的id
    :param public_id: 发送群聊的id
    :param public_msg: 返回给QQ群里展示的信息
    :param private_msg: 返回给私聊的信息
    :param code: 状态码, 目前无使用,默认就好
    :return:
    """
    if need is None:
        need = {}
    return_data = {
        "message":
            {
                "public": public_msg,
                "private": private_msg,
                "public_id": public_id,
                "private_id": private_id},
        'code': code
    }
    return_data = {**return_data, **need}
    return return_data


def is_regis(func):
    """
    装饰器, 检查调用进入某方法的用户是否已注册
    需要装饰几乎所有被 Main 入口调用的方法
    :param func: 被装饰的方法,也就是用户进入的方法
    :return:
    """

    def inner(user_id, *args, **kwargs):
        """
        查询数据库中"u"库,是否包含该用户信息,若无,则返回需要注册,有则代表已注册,执行被装饰的方法,返回其返回结果
        :param user_id:
        :param args:
        :param kwargs:
        :return:
        """
        if not select_u_for_sql(user_id, 'id'):
            return get_return('您还没有注册，请先注册')
        return func(user_id, *args, **kwargs)

    return inner


def is_daily(func):
    """
    装饰器, 检查调用进入某方法的用户是否已签到
    需要装饰所有被 Main 入口调用,且需要花费积分的方法
    :param func: 被装饰的方法,也就是用户进入的方法
    :return:
    """

    def inner(user_id, *args, **kwargs):
        """
        类似,检查"u"表中用户的签到日期,若与今天相同,则已签到,执行被装饰函数,否则返回需要签到
        :param user_id:
        :param args:
        :param kwargs:
        :return:
        """
        # da = select_u_for_sql(user_id, 'da')[0]
        # today = str(datetime.date.today())
        # if da != today:
        #     return get_return('需要先签到的说~')
        return func(user_id, *args, **kwargs)

    return inner


def is_admin(func):
    """
    检查进入方法的用户是否为管理员
    :param func:
    :return:
    """

    def inner(user_id, *args, **kwargs):
        """
        类似,检查"u"表中用户的"permission"字段,若为"admin"则放行,不然返回pa,
        :param user_id:
        :param args:
        :param kwargs:
        :return:
        """
        permission = select_u_for_sql(user_id, 'permission')
        if not permission or permission != ('admin',):
            return get_return('爬')
        return func(user_id, *args, **kwargs)

    return inner


def str_to_python_code(_str1):
    """
    将字符串转为python代码并执行
    :param _str1: 传入的字符串
    :return:
    """
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
    """
    查询积分, 调用sql模块方法
    :param user_id:
    :return:
    """
    score = select_u_for_sql(user_id, 'score')[0]
    return score


def change_score(user_id, score, today=''):
    """
    直接将用户积分更改为某个数
    :param user_id:
    :param score: 需要更改的积分数量
    :param today: 可选,是否为签到时调用的
    :return:
    """
    if score < 0:
        score = 0
    if today:
        update_data = {'score': score, 'da': today}
    else:
        update_data = {'score': score}
    update_u_for_sql(user_id, update_data)


def add_score(user_id, add_score_num):
    """
    给用户增加积分
    :param user_id:
    :param add_score_num: 增加的积分数量
    :return:
    """
    old_score = select_score(user_id)
    if add_score_num + old_score < 0:
        add_score_num = 0
    else:
        add_score_num += old_score
    update_u_for_sql(user_id, {"score": add_score_num})


def enough_score(user_id, score):
    """
    检查用户的积分是否够某个消费的积分
    :param user_id:
    :param score: 需要消费的积分
    :return:
    """
    score1 = select_score(user_id)
    if score1 >= score:
        return score1
    return False


if __name__ == '__main__':
    str1 = """print(136845)"""
    a = str_to_python_code(str1)
    print(a)
