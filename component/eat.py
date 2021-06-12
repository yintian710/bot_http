# -*- coding: utf-8 -*-
"""
@File  : eat.py
@Author: yintian
@Date  : 2021/6/11 23:43
@Desc  : 
"""
import json
import time

from tool.common import is_regis, get_return
from tool.sql import select_eat, update_eat


def get_restaurants_data(user_id):
    """
    获取用户所有食府数据
    :param user_id:
    :return:
    """
    restaurants = select_eat(user_id, 'restaurants')[0]
    restaurants = json.loads(restaurants)
    return restaurants


def save_restaurants_data(user_id, restaurants_data):
    """
    存储用户更改后的食府数据
    :param user_id:
    :param restaurants_data:
    :return:
    """
    restaurants_data = json.dumps(restaurants_data)
    update_eat(user_id, {'restaurants': restaurants_data, 'active': time.time()})


def get_restaurants_did(user_id):
    """
    获取用户历史数据
    :param user_id:
    :return:
    """
    did = select_eat(user_id, 'did')
    did = json.loads(did)
    return did


def save_restaurants_did(user_id, did):
    """
    保存用户历史数据
    :param user_id:
    :param did:
    :return:
    """
    did = json.dumps(did)
    update_eat(user_id, {'did': did, 'active': time.time()})


def get_one_restaurant(restaurants_data, restaurant_id):
    """
    获取单个食府数据
    :param restaurants_data:
    :param restaurant_id:
    :return:
    """
    restaurant = restaurants_data.get(restaurant_id)
    return restaurant


def get_restaurant(user_id):
    restaurant_number = get_restaurant_id(user_id)
    restaurant = get_one_restaurant(user_id, restaurant_number)
    return restaurant


def get_restaurant_id(user_id):
    restaurants_data = get_restaurants_data(user_id)
    restaurant_id = restaurants_data.get("0")
    return restaurant_id


def choose_restaurant(user_id, restaurants_data, restaurant_id):
    restaurants_data['0'] = restaurant_id
    save_restaurants_data(user_id, restaurants_data)


if __name__ == '__main__':
    pass
