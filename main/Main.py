# -*- coding: utf-8 -*-
"""
@File  : Main.py
@Author: yintian
@Date  : 2021/3/31 15:05
@Desc  : 主方法,在这里面写入方法入口,与http通信
"""

from flask import Flask, request

from component.boom import boom_play, new_boom
from component.card import search_card, draw_card, draw_ten_card, draw_hundred_card, get_card_data
from component.score import daily_score, search_score, increase_score

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/score/daily/', methods=['POST'])
def score_daily():
    """
    签到入口
    :return:
    """
    user_id = request.form['user_id']
    result = daily_score(user_id)
    return result


@app.route('/score/search/', methods=['POST'])
def score_search():
    """
    查询积分入口
    :return:
    """
    user_id = request.form['user_id']
    result = search_score(user_id)
    return result


@app.route('/score/admin_increase/', methods=['POST'])
def admin_increase():
    """
    管理员插入积分入口
    :return:
    """
    user_id = request.form['user_id']
    score = int(request.form['score'])
    result = increase_score(user_id, score)
    return result


@app.route('/card/search/', methods=['POST'])
def card_search():
    """
    查询卡牌入口
    :return:
    """
    user_id = request.form['user_id']
    result = search_card(user_id)
    return result


@app.route('/card/draw', methods=['POST'])
def draw():
    """
    抽卡入口
    :return:
    """
    user_id = request.form['user_id']
    result = draw_card(user_id)
    return result


@app.route('/card/draw_ten', methods=['POST'])
def draw_ten():
    """
    十连抽入口
    :return:
    """
    user_id = request.form['user_id']
    result = draw_ten_card(user_id)
    return result


@app.route('/card/draw_hundred', methods=['POST'])
def draw_hundred():
    """
    百连抽入口
    :return:
    """
    user_id = request.form['user_id']
    result = draw_hundred_card(user_id)
    return result


@app.route('/card/get_data', methods=['POST'])
def card_get_data():
    """
    获取卡牌base64内容入口
    :return:
    """
    user_id = request.form['user_id']
    card = request.form['card']
    result = get_card_data(user_id, card)
    return result


@app.route('/boom/new', methods=['POST'])
def new():
    """

    :return:
    """
    # user_id = request.form['user_id']
    result = new_boom()
    return result


@app.route('/boom/play', methods=['POST'])
def play():
    user_id = request.form['user_id']
    boom_num = request.form['boom_num']
    result = boom_play(user_id, boom_num)
    return result


if __name__ == '__main__':
    # 运行flask.app
    app.run(host='0.0.0.0', port=4399)
