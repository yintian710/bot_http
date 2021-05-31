# -*- coding: utf-8 -*-
"""
@File  : wx.py
@Author: yintian
@Date  : 2021/5/17 22:40
@Desc  : 
"""
import requests

from .tool import *


@on_command('wx_regis_code', aliases=('#获取验证码'), only_to_me=False)
async def card(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    data = {'user_id': user_id}
    res = requests.post('https://wxbot.yintian.vip:4399/wx/get_verify_code', data=data)
    if res.status_code != 200:
        await session.send('获取失败，请稍候重试', at_sender=True)
        return
    data_ = res.json()
    await session.send(data_['message']['private'], at_sender=True)


if __name__ == '__main__':
    user_id = 1327960105
    data = {'user_id': user_id}
    res = requests.post('https://wxbot.yintian.vip:4399/wx/get_verify_code', data=data)
    if res.status_code != 200:
        # await session.send('获取失败，请稍候重试', at_sender=True)
        # return
        print('获取失败，请稍候重试')
    data_ = res.json()
    print(data_)
