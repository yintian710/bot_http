# coding:utf-8
import random
import time

from tool.common import get_return, is_regis, is_daily, enough_score
from tool.CONTANT import BOOM_SCORE, BOOM_PRICE
from tool.common import add_score

boom = 0
left = 0
right = 100
player = [{'user_id': '', "time": 0}]


def can_to_int(int1):
    """

    :param int1:
    :return:
    """
    try:
        int1 = int(int1)
    except Exception as e:
        print(e)
        int1 = 0
    return int1


def new_boom():
    """
    新建一个boom数,并将它设为全局变量
    但是,在boom不为0的时候,要拒绝这个请求
    :return:
    """
    global boom
    if boom == 0:
        boom = random.randint(1, 99)
        return get_return('游戏创建成功！')
    else:
        return get_return('已经有游戏正在进行！')


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
    判断boom_num与boom的大小,并提示接下来的游戏范围,当一个人猜对时,归零boom
    :param user_id:
    :param boom_num:
    :return:
    """
    global boom, left, right
    boom_num = can_to_int(boom_num)
    res = is_not_continue(user_id)
    if res:
        return res
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
        boom = 0
        left = 0
        right = 100
        add_score(user_id, BOOM_SCORE)
        str1 = get_return(f'恭喜你答对了, 获得积分{BOOM_SCORE}')
    player.append({"user_id": user_id, "time": time.time()})
    return str1
