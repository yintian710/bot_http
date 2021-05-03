# -*- coding: utf-8 -*-
"""
@File  : boom.py
@Author: yintian
@Date  : 2021/5/03 15:40
@Desc  : 完成了boom游戏的大部分内容，目前还需要完成一个玩家短时间内游玩两次的拒绝
         然后还需要创建一个Main中的入口：new_user_boom， url为：127.0.0.1:4399/boom/user_boom
"""
import random
import time

from tool.common import get_return, is_regis, is_daily, enough_score, add_score
from tool.CONTANT import BOOM_SCORE, BOOM_PRICE, USER_BOOM_PRICE, pa, USER_BOOM_TAX
from tool.sql import select_game_for_sql, update_game_for_sql

# 炸弹数
boom = 0

# 左右区间
left = 0
right = 100

# 存储本场游戏的游玩玩家列表，用于检测玩家当前是否可以进行游戏
player = [{'user_id': '', "time": 0}]

# 当游戏为玩家开启时，此标量存储开启玩家user_id
boom_owner = 0

# 0表示游戏未开始， 1表示游戏由系统开启， 简称系统游戏， 2表示游戏由玩家开启， 简称玩家游戏
boom_type = 0

# boom本场游戏中，玩家所花费的积分，可用于玩家游戏的结算
boom_consume = 0


def to_zero():
    """
    置零所有boom相关参数
    :return:
    """
    global boom, boom_owner, boom_type, boom_consume, player, left, right
    boom = 0
    left = 0
    right = 100
    boom_type = 0
    boom_owner = 0
    boom_consume = 0
    player = [{'user_id': '', "time": 0}]


def can_to_int(int1):
    """
    检查int1是否可以转换为数字，若是，返回转换之后的结果，否则返回0
    :param int1:
    :return:
    """
    try:
        int1 = int(int1)
    except Exception as e:
        print(e)
        int1 = 0
    return int1


def get_reward_score(left, right):
    """
    依据答对时的区间决定奖励积分数
    :param left:
    :param right:
    :return:
    """
    if right - left == 100:
        reward_score = 66
    elif right - left >= 80:
        reward_score = 40
    elif right - left >= 30:
        reward_score = 24
    elif right - left >= 20:
        reward_score = 20
    elif right - left >= 10:
        reward_score = 14
    elif right - left > 3:
        reward_score = 10
    elif right - left == 3:
        reward_score = 8
    else:
        reward_score = 6
    return reward_score


def new_boom(user_id):
    """
    新建一个boom数,并将它设为全局变量
    但是,在boom不为0的时候,要拒绝这个请求
    同时每个玩家一天只能开启一次系统游戏，所以:
    在开启游戏前需要检测game的boom字段,若不为0,则代表当前玩家今日开启过数字炸弹，拒绝该请求
    开启游戏后将数据库game表中的"boom"字段设为1
    :return:
    """
    global boom, boom_type
    if not boom_type:
        if select_game_for_sql(user_id, 'boom'):
            return pa
        to_zero()
        boom = random.randint(1, 99)
        boom_type = 1
        update_game_for_sql(user_id, {'boom': 1})
        return get_return('游戏创建成功！')
    return get_return('已经有游戏正在进行！')


@is_regis
@is_daily
def new_user_boom(user_id, user_boom=0, group_id=''):
    """
    玩家开启数字炸弹，并且将boom设置为玩家定好的数字
    要是存在group_id，则随机设定boom
    同时设定boom_owner和boom_type
    :param user_id:
    :param user_boom:
    :param group_id:
    :return:
    """
    global boom, boom_owner, boom_type
    user_boom = can_to_int(user_boom)
    if boom_type:
        return get_return('已经有游戏正在进行！')
    to_zero()
    if not 0 < user_boom < 100:
        return get_return('给爷爬！游戏范围都不知道了？')
    to_zero()
    boom = user_boom
    if group_id:
        boom = random.randint(1, 99)
    score = enough_score(user_id, USER_BOOM_PRICE)
    if not score:
        # 此处预留银行贷款功能，等银行写好后再补充
        return pa
    add_score(user_id, -USER_BOOM_PRICE)
    boom_owner = user_id
    boom_type = 2
    return get_return('创建成功')


def is_not_continue(user_id):
    """
    验证游戏是否可以继续玩
    :param user_id:
    :return:
    """
    if not boom:
        return get_return('没有游戏进行')
    if not enough_score(user_id, BOOM_PRICE):
        return get_return('积分不足！')
    return False


@is_regis
@is_daily
def boom_play(user_id, boom_num):
    """
    判断boom_num与boom的大小,并提示接下来的游戏范围,当一个人猜对时,置零所有参数
    :param user_id:
    :param boom_num:
    :return:
    """
    global boom, left, right, boom_type, boom_consume
    boom_num = can_to_int(boom_num)
    res = is_not_continue(user_id)
    if res:
        return res
    boom_consume += BOOM_PRICE
    add_score(user_id, -BOOM_PRICE)
    if not left < boom_num < right:
        player.append({"user_id": user_id, "time": time.time()})
        return get_return(f'猜错了，接下请从[{left}-{right}]选择')
    if boom_num < boom:
        left = boom_num
        str1 = get_return(f'猜错了，接下请从[{left}-{right}]选择')
    elif boom_num > boom:
        right = boom_num
        str1 = get_return(f'猜错了，接下请从[{left}-{right}]选择')
    else:
        reward_score = get_reward_score(left, right)
        add_score(user_id, reward_score)
        if boom_type == 2:
            owner_score = USER_BOOM_PRICE + boom_consume - reward_score - USER_BOOM_TAX
            str1 = get_return(public_msg=f'恭喜你答对了, 获得积分{BOOM_SCORE}',
                              private_msg=f'您做庄的数游戏已结束,扣除4积分启动分，玩家获胜分{reward_score}\n'
                              f'玩家总参与积分{boom_consume}\n返还给您{owner_score}积分。',
                              private_id=boom_owner)
            add_score(boom_owner, owner_score)
        else:
            str1 = get_return(public_msg=f'恭喜你答对了, 获得积分{BOOM_SCORE}')
        to_zero()
    player.append({"user_id": user_id, "time": time.time()})
    return str1
