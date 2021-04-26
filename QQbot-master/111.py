# coding=utf-8
import os

import pymysql
import datetime
from random import sample

# gp = ['xxr', 'cc', 'ddz', 'xxm', 'sdqw', 'kz', 'htl27', 'sjdd460', 'xk']
con = pymysql.connect(host='localhost', user='root', password='282610', database='qqbot', charset='utf8')
cur = con.cursor()


def gg(base, id, user_id, x, y):  # 更改 x为需要更改的属性，y为改后的值
    sql = f"update {base} set {x}={y} where {id}='{user_id}'"
    print(sql)
    cur.execute(sql)
    con.commit()


def ye(user_id, x):
    jf = int(select('u', 'score', 'id', user_id)[0])
    id = 'id'
    sql = f"update u set score ={jf + x} where {id}='{user_id}'"
    cur.execute(sql)
    con.commit()


def select(base, x, a, b):
    cur.execute(f'select {x} from {base} where {a} = {b}')
    res = cur.fetchone()
    con.commit()
    return res


achieve_list = {
    '全卡牌终极玩家': 2000,
    '终极460': 100,
    '高级460': 500,
    '中级460': 200,
    '狮子CP团': 100,
    '防道少女团': 200,
    '视角姬女仆团': 200,
    # '女仆长': ['欠欠——独立女仆长'],
    '四大欠王': 200,
    '狮林国际': 200,
    '半壁江山': 300,
    '0+7狂热者': 300,
    '小潮工作室': 150,
    'coser爱好者': 100,
    '车模爱好者': 100,
    '帝王蟹爱好者': 100,
    '萌宠爱好者': 100,
    '猎奇控': 100,
    '物品收集者': 100
    }

cur.execute('select id,score,N,R,SR,SSR,UR,achievement from u')
user = cur.fetchall()
dic = {}

# for i in user:
#     ach = ''
#     user_id = i[0]
#     print(user_id)
#     cur.execute(f'select achievement from u where id = {user_id}')
#     res = cur.fetchone()
#     card = {}
#     if res:
#         print(res)
#         res_achieve = res[0].split(' ')
#         print(res_achieve)
#         dic[user_id] = [len(res_achieve), res_achieve]

def sort_root(res):
    print(dic[res][0])
    return int(dic[res][0])


# dic1 = sorted(dic, key=sort_root, reverse=False)
#
# for i in dic1:
#     print(i, dic[i])
for _ in user:
    # dic[_[0]] = _[1] + _[2]*2 + _[3]*5 + _[4]*10 + _[5]*30 + _[6]*100
    # for i in achieve_list:
    #     if _[7] and i in _[7]:
    #         dic[_[0]] += achieve_list[i]
    cur.execute(f'update u set achievement="" where id={_[0]}')
    con.commit()
print(dic)
