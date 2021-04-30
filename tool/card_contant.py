# -*- coding: utf-8 -*-
"""
@File  : card_contant.py
@Author: yintian
@Date  : 2021/4/26 22:23
@Desc  : 
"""
import json
from tool.CONTANT import IMG_PATH

# 读取卡牌内容,存为dict格式

with open(IMG_PATH['UR'], 'r') as f:
    UR_img = json.loads(f.read())

with open(IMG_PATH['SSR'], 'r') as f:
    SSR_img = json.loads(f.read())

with open(IMG_PATH['SR'], 'r') as f:
    SR_img = json.loads(f.read())

with open(IMG_PATH['R'], 'r') as f:
    R_img = json.loads(f.read())

with open(IMG_PATH['N'], 'r') as f:
    N_img = json.loads(f.read())


# 获取每种卡牌的数量

N_num = len(N_img)
R_num = len(R_img)
SR_num = len(SR_img)
SSR_num = len(SSR_img)
UR_num = len(UR_img)

# 获取卡牌的等级字典,全卡牌列表

card_img = {'UR': UR_img, 'SSR': SSR_img, 'SR': SR_img, 'R': R_img, 'N': N_img}
card_level = [UR_img, SSR_img, SR_img, R_img, N_img]


# 获取每个卡牌名称对应的卡牌等级的dict

level = {}
for _ in card_img:
    for card in card_img[_]:
        level[card] = _

if __name__ == '__main__':
    pass
