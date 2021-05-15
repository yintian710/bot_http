# -*- coding: utf-8 -*-
"""
@File  : wx.py
@Author: yintian
@Date  : 2021/5/13 19:14
@Desc  : 
"""
import requests

from tool.common import get_return


def get_login_openid(data):
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    params = data
    res = requests.get(url, params=params)
    if res.status_code != 200:
        return get_return('获取失败', code=1)
    data_json = res.json()
    if data_json.get('openid'):
        return get_return('获取成功', need=res.json())
    else:
        return get_return('获取失败', code=1)


if __name__ == '__main__':
    pass
