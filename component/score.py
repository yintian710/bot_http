# -*- coding: utf-8 -*-
"""
@File  : score.py
@Author: yintian
@Date  : 2021/3/31 15:19
@Desc  : 
"""
import datetime
import json
import random

from tool.common import get_return, is_regis, change_score, select_score, enough_score, is_admin, add_score
from tool.sql import select_u


@is_regis
def daily_score(user_id):
    """
    签到,检查是否已签到,未签到则产生随机积分,并将积分赋给该用户,更改该用户的"score"积分字段以及"da"签到日期字段
    :param user_id:
    :return:
    """
    score, da = select_u(user_id, 'score', 'da')
    today = str(datetime.date.today())
    # if da == today:
    #     return get_return('臭不要脸签两次的爬！', 1)
    a = random.randint(20, 50)
    if a <= 24:
        str2 = '不会真有人觉得自己签个到就能欧皇吧？不会吧不会吧？\n非酋签个到也才'
    elif a >= 41:
        str2 = '欧皇ohhh!!\n签到居然有'
    else:
        str2 = '...\n获得:'
    # if score >= 500:
    #     a = int(a*0.1)
    #     str1 = '\n积分超过五百，签到积分减少90%，'
    # elif score >= 400:
    #     a = int(a*0.6)
    #     str1 = '\n积分超过四百，签到积分减少60%,'
    # elif score >= 300:
    #     a = int(a*0.5)
    #     str1 = '\n积分超过三百，签到积分减少50%,'
    # elif score >= 200:
    #     a = int(a*0.6)
    #     str1 = '\n积分超过二百，签到积分减少40%,'
    score += a
    change_score(user_id, score, today)
    return get_return(str2 + f'{a}积分！总积分:{score}')


@is_regis
def search_score(user_id):
    """
    查询用户积分
    :param user_id:
    :return:
    """
    score = select_score(user_id)
    if score:
        return get_return(f'积分：{score}', need={'score': score})
    return '穷鬼爬'


@is_regis
def get_score(user_id):
    """
    返回纯净可操作性的积分数额
    :param user_id:
    :return:
    """
    score = select_score(user_id)
    return json.dumps({'score': score})


@is_admin
def increase_score(user_id, score):
    """
    直接插入积分, 管理员专用
    :param user_id:
    :param score:
    :return:
    """
    add_score(user_id, score)
    return get_return('增加成功')


if __name__ == '__main__':
    daily_score(132796010)
