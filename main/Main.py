# -*- coding: utf-8 -*-
"""
@File  : Main.py
@Author: yintian
@Date  : 2021/3/31 15:05
@Desc  :
"""

from flask import Flask, request

from component.card import search_card, draw_card, draw_ten_card, draw_hundred_card, get_card_data
from component.score import daily_score, search_score, increase_score

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/score/daily/', methods=['POST'])
def score_daily():
    user_id = request.form['user_id']
    result = daily_score(user_id)
    return result


@app.route('/score/search/', methods=['POST'])
def score_search():
    user_id = request.form['user_id']
    result = search_score(user_id)
    return result


@app.route('/score/admin_increase/', methods=['POST'])
def admin_increase():
    user_id = request.form['user_id']
    score = int(request.form['score'])
    result = increase_score(user_id, score)
    return result


@app.route('/card/search/', methods=['POST'])
def card_search():
    user_id = request.form['user_id']
    result = search_card(user_id)
    return result


@app.route('/card/draw', methods=['POST'])
def draw():
    user_id = request.form['user_id']
    result = draw_card(user_id)
    return result


@app.route('/card/draw_ten', methods=['POST'])
def draw_ten():
    user_id = request.form['user_id']
    result = draw_ten_card(user_id)
    return result


@app.route('/card/draw_hundred', methods=['POST'])
def draw_hundred():
    user_id = request.form['user_id']
    result = draw_hundred_card(user_id)
    return result


@app.route('/card/get_data', methods=['POST'])
def card_get_data():
    user_id = request.form['user_id']
    card = request.form['card']
    result = get_card_data(user_id, card)
    return result


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4399)
