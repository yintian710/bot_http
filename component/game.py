# -*- coding: utf-8 -*-
"""
@File  : game.py
@Author: yintian
@Date  : 2021/3/31 17:30
@Desc  : 
"""
from tool.CONTANT import RUMOR_PRICE
from tool.common import is_regis, enough_score, get_return


@is_regis
def rumor(user_id, message):
    score = enough_score(user_id, RUMOR_PRICE)
    if not score:
        return get_return('爬')


if __name__ == '__main__':
    pass
