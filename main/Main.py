# -*- coding: utf-8 -*-
"""
@File  : Main.py
@Author: yintian
@Date  : 2021/3/31 15:05
@Desc  :
"""

from flask import Flask, request

from component.card import search_card
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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4399)
