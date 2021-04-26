import datetime
import os
import random
import re
import time as ttt
from random import sample
import aiocqhttp
import asyncio
import nonebot
import pymysql
from nonebot import (CommandSession, NoticeSession, on_command, on_notice, permission)
from nonebot.typing import Context_T

from .achieve import achieve_list
from .txt import *

con = pymysql.connect(host='localhost', user='root', password='282610', database='qqbot', charset='utf8')
cur = con.cursor()
# gp = ['xxr', 'cc', 'ddz', 'xxm', 'sdqw', 'kz', 'htl27', 'sjdd460', 'xk']
UR_img = os.listdir(r'C:\Users\Administrator\Desktop\bot\data\images\ck\card\UR')
SSR_img = os.listdir(r'C:\Users\Administrator\Desktop\bot\data\images\ck\card\SSR')
SR_img = os.listdir(r'C:\Users\Administrator\Desktop\bot\data\images\ck\card\SR')
R_img = os.listdir(r'C:\Users\Administrator\Desktop\bot\data\images\ck\card\R')
N_img = os.listdir(r'C:\Users\Administrator\Desktop\bot\data\images\ck\card\N')
N_num = len(N_img)
R_num = len(R_img)
SR_num = len(SR_img)
SSR_num = len(SSR_img)
UR_num = len(UR_img)
cur.execute("select GROUP_CONCAT(COLUMN_NAME) from information_schema.COLUMNS where table_name = 'card'")
# a = cur.fetchall()
# print(a)
cardlist = cur.fetchone()[0].split(',')
card_img = {'UR': UR_img, 'SSR': SSR_img, 'SR': SR_img, 'R': R_img, 'N': N_img}
card_level = [UR_img, SSR_img, SR_img, R_img, N_img]
re_price = {'N': 1, 'R': 3, 'SR': 7}


bot = nonebot.get_bot()
newgame = ' '
card_price = 3
house_price = 5
direction_dic = {0: '无', 1: '制造业', 2: '农业', 3: '服务业'}


things = {0: '无事发生',
          1: '暴风雨, 所有没住房的人需花费15积分购买雨伞。',
          2: '龙卷风，所有没住房的人损失25%的积分。',
          3: '雷电纵横, 租房者因雷电打在了家中,获得物业赔偿10',
          4: '地震，所有住房被摧毁，所有人失去住所，无住所的人有百分之五十的概率失去百分之20的积分。',
          5: '市长巡查，觉得没住所的人很可怜，就把他们关进了监狱。'
          }


def cardlevel(list1):
    if list1 == N_img:
        return 'N'
    if list1 == R_img:
        return 'R'
    if list1 == SR_img:
        return 'SR'
    if list1 == SSR_img:
        return 'SSR'
    if list1 == UR_img:
        return 'UR'


level = {}
for _ in cardlist[1:]:
    for i in card_level:
        if _+'.jpg' in i:
            level[_] = cardlevel(i)
print(level)
print(len(level))
print(cardlist)

def nums(x):
    num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(len(num)):
        num[i] = str(num[i])
    st = ''
    for i in x:
        if i in num:
            st += i
        # print(i)
    return st


def gg(base, id, user_id, x, y):  # 更改 x为需要更改的属性，y为改后的值
    sql = f"update {base} set {x}='{y}' where {id}='{user_id}'"
    print(sql)
    cur.execute(sql)
    con.commit()


def select(base, x, a, b):
    sql = f'select {x} from {base} where {a} = {b}'
    print(sql)
    cur.execute(sql)
    res = cur.fetchone()
    con.commit()
    return res


def zjjf(user_id, x):  # 更改 x为需要更改的属性，y为改后的值
    jf = int(select('u', 'score', 'id', user_id)[0])
    id = 'id'
    sql = f"update u set score ={jf + x} where {id}='{user_id}'"
    cur.execute(sql)
    con.commit()


def kcjf(user_id, x):  # 更改 x为需要更改的属性，y为改后的值
    jf = int(select('u', 'score', 'id', user_id)[0])
    if jf < x:
        jf = x
    id = 'id'
    sql = f"update u set score ={jf - x} where {id}='{user_id}'"
    cur.execute(sql)
    con.commit()


def dtf(dic):  # 元祖转化成数字
    list1 = []
    for i in range(1, len(dic)):
        list1.append(float(dic[i]))
    return list1


def sspeed():
    cn = pymysql.connect(host='localhost', user='root', password='282610', database='qqbot', charset='utf8')
    cu = cn.cursor()
    cu.execute(f'select * from con where id = "speed"')
    s = cu.fetchone()
    con.commit()
    cu.close()
    cn.close()
    return dtf(s)


def dj(id):
    cur.execute(f'select * from jysc where user_id = "{id}" and sell = "0"')
    zs = cur.fetchall()
    print(zs)
    dj1 = 0
    for _ in zs:
        dj1 += _[2]*int(_[3])
    gg('u', 'id', id, 'dj', dj1)


def sodds():
    cn = pymysql.connect(host='localhost', user='root', password='282610', database='qqbot', charset='utf8')
    cu = cn.cursor()
    cu.execute(f'select * from con where id = "odds"')
    s = cu.fetchone()
    con.commit()
    cu.close()
    cn.close()
    return dtf(s)


def sgg():
    list1 = sample(range(1, 7), 6)
    cur.execute('select * from con where id = "odds1"')
    res = cur.fetchone()
    cur.execute(
        f'update con set 6号={res[list1[1]]},2号={res[list1[2]]},3号={res[list1[3]]},4号={res[list1[4]]},5号={res[list1[5]]},1号={res[list1[0]]} where id = "odds"')
    con.commit()
    cur.execute('select * from con where id = "speed1"')
    res = cur.fetchone()
    cur.execute(
        f'update con set 6号={res[list1[1]]},2号={res[list1[2]]},3号={res[list1[3]]},4号={res[list1[4]]},5号={res[list1[5]]},1号={res[list1[0]]} where id = "speed"')
    con.commit()


def xwzu(user_id, ma, jf):
    pass
    cur.execute(f'select * from xz where id = {user_id}')
    data = cur.fetchone()
    print(data)
    if not data:
        cur.execute(f'insert into xz value({user_id},{jf},{ma})')
    elif data[2] == ma:
        cur.execute(f'update xz set ma={ma},jf=jf+{jf} where id={user_id}')
    else:
        cur.execute(f'update xz set ma={ma},jf={jf} where id={user_id}')
    con.commit()


def minnum(user_id, num):
    pass
    cur.execute(f'select * from mins where id = {user_id}')
    data = cur.fetchone()
    print(data)
    if not data:
        cur.execute(f'insert into mins value({user_id},{num})')
    else:
        cur.execute(f'update mins set score={num} where id={user_id}')
    con.commit()


def delete(base):
    cur.execute(f'delete from {base}')
    con.commit()


def horse_t():
    cur.execute('select con from con where id = "horse"')
    res = cur.fetchone()[0]
    print(type(res), res)
    con.commit()
    if res == 0:
        return False
    elif res == 1:
        return True


def horse_set(n):
    cur.execute(f'update con set con={n} where id="horse"')
    con.commit()

def ye(user_id):
    score = int(select('u', 'score', 'id', user_id)[0])
    return score

def day(user_id):
    s = 'select da from u where id = %s' % user_id
    cur.execute(s)
    con.commit()
    res = str(cur.fetchone()[0])
    today = str(datetime.date.today())
    if res == today:
        return False
    else:
        return True

@on_command('sql', aliases=('sql',), permission=permission.SUPERUSER)
async def sql(session: CommandSession):
    global cur, con
    try:
        cur.close()
        con.close()
    except:
        pass
    con = pymysql.connect(host='localhost', user='root', password='282610', database='qqbot', charset='utf8')
    cur = con.cursor()


@on_command('s', aliases=('s',), permission=permission.SUPERUSER)
async def s(session: CommandSession):
    await session.send(f'{type(session.ctx.group_id)}')


@on_notice('group_increase')
async def _(session: NoticeSession):
    await session.send('欢迎新朋友～')


# if __name__ == '__main__':
#     sql()
