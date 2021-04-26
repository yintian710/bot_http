#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-04-24
@file: card.py
"""
from tool.common import is_regis, get_return, is_daily, select_score, add_score
from tool.sql import select_card_for_sql, select_u_for_sql, update_card_for_sql, update_u_for_sql
from tool.card_contant import *
from random import choice, randint
from tool.CONTANT import CARD_PRICE


@is_regis
def search_card(user_id):
    res = select_u_for_sql(user_id, 'N', 'R', 'SR', "SSR", 'UR')
    str1 = f'N:{res[0]}  R:{res[1]}  SR:{res[2]}  SSR:{res[3]}  UR:{res[4]}'
    return get_return(str1)


@is_regis
def archive_card(user_id, img, lv, num=1):
    if '.jpg' in img:
        img = img[:-4]
    img_num = select_card_for_sql(user_id, img)
    lv_num = select_u_for_sql(user_id, lv)
    update_card_for_sql({"id": user_id}, {img: img_num + num})
    update_u_for_sql(user_id, {lv: lv_num + num})


@is_regis
def get_random_card():
    UR = UR_num
    SSR = UR + SSR_num * 3
    SR = SSR + SR_num * 9
    R = SR + R_num * 27
    N = R + N_num * 81
    a = randint(0, N)
    if a < UR:
        img = choice(UR_img)
        str1 = '获得UR!!!欧皇再世！——' + img[:-4]
        lv = 'UR'
    elif a < SSR:
        img = choice(SSR_img)
        str1 = '获得SSR!!!——' + img[:-4]
        lv = 'SSR'
    elif a < SR:
        img = choice(SR_img)
        str1 = '获得SR!——' + img[:-4]
        lv = 'SR'
    elif a < R:
        img = choice(R_img)
        str1 = '获得R!——' + img[:-4]
        lv = 'R'
    else:
        img = choice(N_img)
        str1 = '获得N!——' + img[:-4]
        lv = 'N'
    return img, str1, lv


@is_daily
def draw_card(user_id):
    score = select_score(user_id)
    if score < CARD_PRICE:
        return get_return('爬')
    add_score(user_id, -CARD_PRICE)
    img, str1, lv = get_random_card()
    str1 = f'花费{CARD_PRICE}积分，获得{lv}卡：{img}。'
    archive_card(user_id, img, lv, 1)
    return get_return(str1)


if __name__ == '__main__':
    pass
