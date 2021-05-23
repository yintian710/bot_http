#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-04-24
@file: card.py
"""
from tool.common import is_regis, is_daily, select_score, add_score, get_return, change_score
from tool.sql import select_card, select_u, update_card, update_u
from tool.card_contant import *
from random import choice, randint
from tool.CONTANT import CARD_PRICE, pa, RE_PRICE


def archive_card(user_id, img, lv, num=1):
    """
    存储抽卡获得的卡牌
    :param user_id:
    :param img: 卡牌名称
    :param lv: 卡牌等级
    :param num: 获得的卡牌数量
    :return:
    """
    if '.jpg' in img:
        img = img[:-4]
    img_num = select_card(user_id, img)[0]
    lv_num = select_u(user_id, lv)[0]
    update_card({"id": user_id}, {img: img_num + num})
    update_u(user_id, {lv: lv_num + num})


def archive_cards(user_id, imgs: dict, lvs: dict):
    """
    存储十连或者是百连获取的卡牌,一次性存储
    :param user_id:
    :param imgs: 卡牌字典,{卡牌名:卡牌数量}
    :param lvs: 卡牌等级,{卡牌等级: 数量}
    :return:
    """
    img_list = list(imgs.keys())
    lv_list = list(lvs.keys())
    img_num = select_card(user_id, *img_list)
    lv_num = select_u(user_id, *lv_list)
    for i, _ in enumerate(img_list):
        imgs[_] += img_num[i]
    for i, _ in enumerate(lv_list):
        lvs[_] += lv_num[i]
    update_card({"id": user_id}, imgs)
    update_u(user_id, lvs)


def get_random_card():
    """
    随机产生随机等级的随机卡牌
    :return:
    """
    UR = UR_num
    SSR = UR + SSR_num * 3
    SR = SSR + SR_num * 9
    R = SR + R_num * 27
    N = R + N_num * 81
    a = randint(0, N)
    if a < UR:
        img = choice(list(UR_img))
        str1 = '获得UR!!!欧皇再世！——' + img
        lv = 'UR'
    elif a < SSR:
        img = choice(list(SSR_img))
        str1 = '获得SSR!!!——' + img
        lv = 'SSR'
    elif a < SR:
        img = choice(list(SR_img))
        str1 = '获得SR!——' + img
        lv = 'SR'
    elif a < R:
        img = choice(list(R_img))
        str1 = '获得R!——' + img
        lv = 'R'
    else:
        img = choice(list(N_img))
        str1 = '获得N!——' + img
        lv = 'N'
    return img, str1, lv


@is_regis
@is_daily
def draw_card(user_id):
    """
    抽卡
    :param user_id:
    :return:
    """
    score = select_score(user_id)
    if score < CARD_PRICE:
        return get_return('爬')
    add_score(user_id, -CARD_PRICE)
    img, str1, lv = get_random_card()
    str1 = f'花费{CARD_PRICE}积分，获得{lv}卡：{img}。'
    archive_card(user_id, img, lv, 1)
    return get_return(str1, need={'card': img})


@is_regis
@is_daily
def draw_ten_card(user_id):
    """
    十连抽
    :param user_id:
    :return:
    """
    score = select_score(user_id)
    if score < CARD_PRICE * 9:
        return get_return('爬')
    add_score(user_id, -9 * CARD_PRICE)
    str1 = f'花费{CARD_PRICE * 9}积分。\n'
    n_NUM = 0
    lv_num = {'UR': 0, "SSR": 0, 'SR': 0, 'R': 0, 'N': 0}
    card_num = {'N': [], 'R': [], 'SR': [], "SSR": [], 'UR': []}
    imgs = {}
    for i in range(10):
        img, str2, lv = get_random_card()
        n_NUM += 1 if lv == 'N' else 0
        if n_NUM == 10:
            while lv == 'N':
                img, str2, lv = get_random_card()
                str1 += '触发保底：\n'
        lv_num[lv] += 1
        if imgs.get(img):
            imgs[img] += 1
        else:
            imgs[img] = 1
        card_num[lv].append(img)
        if str2:
            str1 += str2 + '\n'
    archive_cards(user_id, imgs, lv_num)
    return get_return(str1)


@is_regis
def search_card(user_id):
    """
    查询用户拥有的卡牌
    :param user_id:
    :return:
    """
    res = select_u(user_id, 'N', 'R', 'SR', "SSR", 'UR')
    str1 = f'N:{res[0]}  R:{res[1]}  SR:{res[2]}  SSR:{res[3]}  UR:{res[4]}'
    return get_return(str1)


@is_regis
@is_daily
def draw_hundred_card(user_id):
    """
    百连抽
    :param user_id:
    :return:
    """
    score = select_score(user_id)
    if score < CARD_PRICE * 80:
        return get_return('爬')
    lv_num = {'UR': 0, "SSR": 0, 'SR': 0, 'R': 0, 'N': 0}
    card_num = {'N': [], 'R': [], 'SR': [], "SSR": [], 'UR': []}
    imgs = {}
    for i in range(100):
        img, str1, lv = get_random_card()
        lv_num[lv] += 1
        if imgs.get(img):
            imgs[img] += 1
        else:
            imgs[img] = 1
        card_num[lv].append(img)
    archive_cards(user_id, imgs, lv_num)
    str1 = f'扣除{CARD_PRICE * 80}积分\n获得UR卡{lv_num["UR"]}张\n获得SSR卡{lv_num["SSR"]}张\n获得SR卡{lv_num["SR"]}张\n' \
        f'获得R卡{lv_num["R"]}张\n获得N卡{lv_num["N"]}张\n详细抽卡结果已私聊发送'
    str3 = ''  # str3 为私聊发送
    for i in card_num:
        if i == 'N':
            str3 += '获得N卡若干\n'
            continue
        if not card_num[i]:
            continue
        for _ in card_num[i]:
            str3 += f'获得{i}——{_}\n'
    return get_return(str1, str3)


@is_regis
def get_card_data(user_id, card_name):
    """
    用卡牌名获取卡牌的base64加密后内容
    :param user_id:
    :param card_name: 卡牌名称
    :return:
    """
    res = select_card(user_id, card_name)[0]
    if res == 0:
        return pa
    card_data = card_img[level[card_name]][card_name]
    return card_data


@is_regis
@is_daily
def sell_card(user_id, card_name, nums=1):
    """
    售卖卡牌
    :param user_id:
    :param card_name: 卡牌名
    :param nums: 售卖的数量
    :return:
    """
    res = select_card(user_id, card_name)[0]
    if res < nums:
        return pa
    sell_score = RE_PRICE[level[card_name]] * nums
    add_score(user_id, sell_score)
    update_card({'user_id': user_id}, {card_name: res - nums})


if __name__ == '__main__':
    pass
