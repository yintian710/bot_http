# -*- coding: utf-8 -*-
"""
@File  : card_contant.py
@Author: yintian
@Date  : 2021/4/26 22:23
@Desc  : 
"""
import json
from tool.CONTANT import IMG_PATH

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

N_num = len(N_img)
R_num = len(R_img)
SR_num = len(SR_img)
SSR_num = len(SSR_img)
UR_num = len(UR_img)

card_img = {'UR': UR_img, 'SSR': SSR_img, 'SR': SR_img, 'R': R_img, 'N': N_img}
card_level = [UR_img, SSR_img, SR_img, R_img, N_img]

if __name__ == '__main__':
    pass
