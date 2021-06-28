# -*- coding: utf-8 -*-
"""
@File  : eat.py
@Author: yintian
@Date  : 2021/6/11 23:43
@Desc  : 
"""
import json
import random
import time

from tool.CONTANT import GO_WEIGHT, NEXT_WEIGHT
from tool.common import is_regis, get_return
from tool.sql import select_eat, update_eat


def get_restaurants_data(user_id) -> dict:
    """
    获取用户所有食府数据
    :param user_id:
    :return:
    """
    restaurants = select_eat(user_id, 'restaurants')[0]
    restaurants = json.loads(restaurants)
    return restaurants


def save_restaurants_data(user_id, restaurants_data) -> None:
    """
    存储用户更改后的食府数据
    :param user_id:
    :param restaurants_data:
    :return:
    """
    restaurants_data = json.dumps(restaurants_data)
    update_eat(user_id, {'restaurants': restaurants_data, 'active': time.time()})


def get_restaurants_did(user_id) -> list:
    """
    获取用户历史数据
    :param user_id:
    :return:
    """
    did = select_eat(user_id, 'did')[0]
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


def save_restaurants_cache(user_id, cache):
    cache = json.dumps(cache)
    update_eat(user_id, {'cache': cache, 'active': time.time()})


def did_restaurant(user_id, food):
    did = get_restaurants_did(user_id)
    did.append({'food': food, 'time': time.time()})
    did = json.dumps(did)
    update_eat(user_id, {'did': did, 'active': time.time()})


def get_one_restaurant(restaurants_data, restaurant_id) -> dict:
    """
    获取单个食府数据
    :param restaurants_data:
    :param restaurant_id:
    :return:
    """
    restaurant = restaurants_data.get(restaurant_id)
    return restaurant


def get_restaurant(user_id) -> dict:
    """
    获取用户当前选定食府数据
    :param user_id:
    :return:
    """
    restaurant_number = get_restaurant_id(user_id)
    restaurant_data = get_restaurants_data(user_id)
    restaurant = get_one_restaurant(restaurant_data, restaurant_number)
    return restaurant


@is_regis
def get_user_restaurant(user_id):
    """
    获取用户食府数据
    :param user_id:
    :return:
    """
    restaurant_id = get_restaurant_id(user_id)
    restaurant = get_restaurant(user_id)
    name = restaurant.get('name')
    food = restaurant.get('food')
    str1 = f'您当前食府为{restaurant_id}号食府{name}，食物为：{"、".join(food.keys())}'
    return get_return(public_msg=str1, need={'restaurant': restaurant})


def get_restaurant_id(user_id) -> str:
    """
    获取当前用户选定食府id
    :param user_id:
    :return:
    """
    restaurants_data = get_restaurants_data(user_id)
    restaurant_id = restaurants_data.get("0")
    return restaurant_id


def choose_restaurant(user_id, restaurants_data, restaurant_id) -> None:
    """
    改变用户当前选定食府id
    :param user_id:
    :param restaurants_data:
    :param restaurant_id:
    :return:
    """
    restaurants_data['0'] = restaurant_id
    save_restaurants_data(user_id, restaurants_data)


def get_random_food(food_dic: dict, ignore=None) -> str:
    """
    获取随即产生的食物
    :param food_dic: 食府中的食物数据
    :param ignore: 需要被忽略的一个食物，往往是已经去了两次的
    :return:
    """
    if ignore:
        food_dic.pop(ignore)
    foods = list(food_dic.keys())
    weights = list(food_dic.values())
    random_food = random.choices(foods, weights=weights)
    return random_food


@is_regis
def go_restaurant(user_id):
    restaurant_id = get_restaurant_id(user_id)
    restaurants_data = get_restaurants_data(user_id)
    go = restaurants_data['go']
    restaurants_data[restaurant_id]['food'][go] += GO_WEIGHT
    restaurants_data['active'] = time.time()
    did_restaurant(user_id, go)
    save_restaurants_data(user_id, restaurants_data)
    restaurants_data['go'] = ''
    return


@is_regis
def next_restaurant(user_id):
    restaurants_data = get_restaurants_data(user_id)
    restaurant_id = get_restaurant_id(user_id)
    now = time.time()
    go = restaurants_data['go']
    if go:
        restaurants_data[restaurant_id]['food'][go] += NEXT_WEIGHT
    food_dic = restaurants_data[restaurant_id]['food']
    did = get_restaurants_did(user_id)
    if (len(did) > 2) and (did[-1]['food'] == did[-2]['food']) and (did[-1]['time'] - did[-2]['time'] < 86400) \
            and (now - did[-1]['time'] < 86400):
        ignore = restaurants_data['go']
    else:
        ignore = None
    food = get_random_food(food_dic, ignore)
    restaurants_data['go'] = food
    restaurants_data['active'] = now
    save_restaurants_data(user_id, restaurants_data)
    return get_return(public_msg=f'当前食物为：{food}', need={'food': food})


@is_regis
def add_restaurants(user_id, add):
    restaurants_data = get_restaurants_data(user_id)
    restaurant_id = get_restaurant_id(user_id)
    restaurant = get_one_restaurant(restaurants_data, restaurant_id)
    add = add.split(' ')
    foods = restaurant['food']
    repeat = ''
    for _ in add:
        if _ in foods:
            repeat += _ + ' '
            continue
        foods[_] = 100
    save_restaurants_cache(user_id, foods)


if __name__ == '__main__':
    res = get_restaurants_data('1327960105')
    print(res)
