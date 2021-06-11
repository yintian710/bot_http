# -*- coding: utf-8 -*-
"""
@File  : eat.py
@Author: yintian
@Date  : 2021/6/11 23:43
@Desc  : 
"""
import json

from tool.common import is_regis, get_return
from tool.sql import select_eat


def get_restaurants(user_id):
    restaurants = select_eat(user_id, 'restaurants')[0]
    restaurants = json.loads(restaurants)
    return restaurants


def get_one_restaurant(user_id, restaurant_id):
    restaurants = get_restaurants(user_id)
    restaurant = restaurants.get(restaurant_id)
    return restaurant


if __name__ == '__main__':
    res = get_one_restaurant("1327960105", "1")
    print(res)
