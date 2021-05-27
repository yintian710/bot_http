# -*- coding: utf-8 -*-
"""
@File  : Main.py
@Author: yintian
@Date  : 2021/3/31 15:05
@Desc  : 主方法,在这里面写入方法入口,与http通信
"""

from flask import Flask, request

from component.achievement import select_achievement, achievement_progress
from component.boom import boom_play, new_boom, new_user_boom
from component.card import search_card, draw_card, draw_ten_card, draw_hundred_card, get_card_data
from component.regis import is_wx_regis, wx_regis, get_verify_code, delete_wx_regis
from component.score import daily_score, search_score, increase_score
from component.wx import get_login_openid
from tool.CONTANT import SSL_KEY_PATH, SSL_PEM_PATH

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/score/daily', methods=['POST'])
def score_daily():
    """
    签到入口
    :return:
    """
    user_id = request.form['user_id']
    result = daily_score(user_id)
    return result


@app.route('/score/search', methods=['POST'])
def score_search():
    """
    查询积分入口
    :return:
    """
    user_id = request.form['user_id']
    result = search_score(user_id)
    return result


@app.route('/score/admin_increase', methods=['POST'])
def admin_increase():
    """
    管理员插入积分入口
    :return:
    """
    user_id = request.form['user_id']
    score_ = int(request.form['score'])
    result = increase_score(user_id, score_)
    return result


@app.route('/card/search', methods=['POST'])
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
    user_id = request.form['user_id']
    result = new_boom(user_id)
    return result


@app.route('/boom/play', methods=['POST'])
def play():
    user_id = request.form['user_id']
    boom_num = request.form['boom_num']
    result = boom_play(user_id, boom_num)
    return result


@app.route('/boom/user_boom', methods=['POST'])
def user_boom():
    """
    user_self_boom:new_user_boom入口
    :return:
    """
    user_id = request.form['user_id']
    user_self_boom = request.form['user_boom']
    result = new_user_boom(user_id, user_self_boom)
    return result


@app.route('/achievement/search', methods=['POST'])
def achieve_search():
    """
    查询成就入口
    :return:
    """
    user_id = request.form['user_id']
    result = select_achievement(user_id)
    return result


@app.route('/achievement/progress', methods=['POST'])
def achieve_one_progress():
    """
    查询成就入口
    :return:
    """
    user_id = request.form['user_id']
    result = achievement_progress(user_id)
    return result


@app.route('/wx/get_open_id', methods=['POST'])
def get_open_id():
    """
    获取微信openid入口
    :return:
    """
    data = request.get_data()
    result = get_login_openid(data)
    return result


@app.route('/wx/is_wx_regis', methods=['POST'])
def get_wx_regis():
    """
    根据微信openid获取是否已经注册的方法入口
    :return:
    """
    openid = request.form['openid']
    result = is_wx_regis(openid)
    return result


@app.route('/wx/wx_regis', methods=['POST'])
def do_wx_regis():
    """
    使用验证码尝试注册
    :return:
    """
    user_id = request.form['user_id']
    verify_code = request.form['verify_code']
    openid = request.form['openid']
    result = wx_regis(user_id, verify_code, openid)
    return result


@app.route('/wx/get_verify_code', methods=['POST'])
def set_verify_code():
    """
    获取验证码
    :return:
    """
    user_id = request.form['user_id']
    result = get_verify_code(user_id)
    return result


@app.route('/wx/delete_wx_regis', methods=['POST'])
def remove_wx_regis():
    """
    注销入口
    :return:
    """
    user_id = request.form['user_id']
    result = delete_wx_regis(user_id)
    return result


if __name__ == '__main__':
    # 运行flask.app
    app.run(host='0.0.0.0', port=4399, ssl_context=(SSL_PEM_PATH, SSL_KEY_PATH))
