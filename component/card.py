#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-04-24
@file: card.py
"""
from tool.common import is_regis, get_return
from tool.sql import select_card_for_sql, select_u_for_sql, update_card_for_sql, update_u_for_sql


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
    update_card_for_sql({"id": user_id}, {img: img_num+num})
    update_u_for_sql(user_id, {lv: lv_num + num})


@is_regis
def get_random_card():
    pass

if __name__ == '__main__':
    pass
