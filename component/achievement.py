#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-04-30
@file: achievement.py
@Desc
"""
from tool.achieve_list import achieve_list
from tool.card_contant import cardlist
from tool.common import get_return, is_regis
from tool.sql import select_u_for_sql, select_card_for_sql, update_u_for_sql


def is_have_zero(list1: list):
    for _ in list1:
        if not _:
            return True
    return False


@is_regis
def select_achievement(user_id):
    """
    查询用户成就
    :param user_id:
    :return:
    """
    achievement = select_u_for_sql(user_id, 'achievement')[0]
    achievement_num = len(achievement.split(' ')) - 1
    str1 = f'您的成就有：{achievement}， 共{achievement_num}个'
    return get_return(str1)


def one_achievement_progress(user_id, achievement):
    """
    检查某个成就的进度
    :param user_id:
    :param achievement: 成就名
    :return:
    """
    cards = select_card_for_sql(user_id, '*')
    card = {}
    for i in range(1, len(cards)):
        card[cardlist[i]] = cards[i]
    is_progress = True
    str1 = f'您的成就 {achievement} 缺少如下卡片:'
    for _ in achieve_list[achievement]:
        if not card[_]:
            is_progress = False
            str1 += _ + ' '
    if is_progress:
        return achievement, ''
    return '', str1 + '\n'


def achievement_progress(user_id):
    """
    检查某用户获得的所有成就
    :param user_id:
    :return:
    """
    str1 = ''
    for _ in achieve_list:
        achieve_name, progress = one_achievement_progress(user_id, _)
        str1 += progress
    return get_return('', str1)


def checks_achieve(user_id):
    """
    由多个卡牌名检查是否需要更新成就
    :param user_id:
    :param card_names: 新获取到的卡牌内容
    :return:
    """
    achievement_list1 = select_u_for_sql(user_id, 'achievement')[0].split(' ')
    achievement_list2 = []
    str_return = ''
    for k, v in achieve_list.items():
        res = select_card_for_sql(user_id, *v)
        if not is_have_zero(res):
            achievement_list2.append(k)
    achievement_set1 = set(achievement_list1)
    achievement_set1.remove('')
    achievement_set2 = set(achievement_list2)
    get_achieve = achievement_set2 - achievement_set1
    lose_achieve = achievement_set1 - achievement_set2
    is_change = False
    if get_achieve:
        str_return += f'恭喜获得新成就{",".join(get_achieve)}'
        is_change = True
    if lose_achieve:
        str_return += f'失去成就{",".join(lose_achieve)}'
        is_change = True
    if is_change:
        update_u_for_sql(user_id, {'achievement': ' '.join(achievement_list2)})


if __name__ == '__main__':
    checks_achieve(1327960105)
