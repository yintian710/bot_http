#coding=utf-8
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

def select(base, x, a, b):
    cur.execute(f'select {x} from {base} where {a} = {b}')
    res = cur.fetchone()
    con.commit()
    return res

# def pfm(gpdm):
#     cur.execute(f'select gpjg from cg where gpdm="{gpdm}"')
#     jg = cur.fetchone()[0]
#     cur.execute(f'select id,{gpdm},score from u')
#     res = cur.fetchall()
#     for i in res:
#         if i[1] != 0:
#             print(i)
#             gg('u', 'id', i[0], gpdm, 0)
#             gg('u', 'id', i[0], 'score', int(i[2])+(i[1]*jg))

# for _ in gp:
#     pfm(_)
# a = '123'
# c = '456'
# b = []
# for i in a+c:
#     b.append(i)
# print(datetime.datetime.now())

# dic = {'金贻凤': 1327960105, '许文韬': 726825474, '何祥': 486582787, '刘臻': 764182578, '张海梦': 1923150783,
#        '符叶': 2693703568, '俞鑫': 137954587, '胡晓涵': 2336782219, '黄俊杰': 1733754966, '刘添逸': 1466753962,
#        '李雄峰': 2608420421, '李晓阳': 1780012858, '黄鑫云': 2408807008, '谷重阳': 2285605872, '殷润': 867712355,
#        '范玉花': 512453469, '陈俊龙': 980112763, '章邦民': 1582671467, '刘淇': 1832891989, '孔志新': 1443497510,
#        '廖新威': 2460296549, '万宇杰': 820239186, '邹玉菲': 1065809244, '杨红晨': 1623137048, '黄文慧': 1641607170,
#        '王凯': 1826400751, '周绍楠': 1979389945, '孙俊': 2632042242, '杨炅': 2966525790, '周宇娇': 3583009402,
#        '陈龙': 3297535188, '彭偲': 1562984817, '张奇': 1804019925}
# print(len(dic))

def zj(name):
    try:
        cur.execute(f'select {name} from card')
        res = cur.fetchone()
    except:
        res = ''
    if not res:
        sql = f"ALTER TABLE card ADD COLUMN {name} int(11) not NULL DEFAULT 0"
        # sql = """ALTER TABLE card ADD COLUMN %s int(11) not NULL DEFAULT 0""" % (pymysql.escape_string(name))
        cur.execute(sql)
        con.commit()
        # print(res)
        print(f'{name}创建成功')
    else:
        print(res)
        print(f'{name}已存在')


UR_img = os.listdir(r'C:\Users\Administrator\Desktop\bot\data\images\ck\card\UR')
SSR_img = os.listdir(r'C:\Users\Administrator\Desktop\bot\data\images\ck\card\SSR')
SR_img = os.listdir(r'C:\Users\Administrator\Desktop\bot\data\images\ck\card\SR')
R_img = os.listdir(r'C:\Users\Administrator\Desktop\bot\data\images\ck\card\R')
N_img = os.listdir(r'C:\Users\Administrator\Desktop\bot\data\images\ck\card\N')
card_level = [UR_img, SSR_img, SR_img, R_img, N_img]
cur.execute("select GROUP_CONCAT(COLUMN_NAME) from information_schema.COLUMNS where table_name = 'card'")
cardlist = cur.fetchone()[0].split(',')
# print()
num = 0
for _ in card_level:
    num += len(_)
    for name in _:
        print(name)
        zj(name[:-4])
print(num)
# cur.close()
# con.close()
card_img = {'UR': UR_img, 'SSR': SSR_img, 'SR': SR_img, 'R': R_img, 'N': N_img}
for _ in card_img:
    print(f'{_}:{card_img[_]}')

# cur.execute("select GROUP_CONCAT(COLUMN_NAME) from information_schema.COLUMNS where table_name = 'card'")
# cardlist = cur.fetchone()[0].split(',')
# print(cardlist)
# print()
# print(len(cardlist))
# def cardlevel(list):
#     if list == N_img:
#         return 'N'
#     if list == R_img:
#         return 'R'
#     if list == SR_img:
#         return 'SR'
#     if list == SSR_img:
#         return 'SSR'
#     if list == UR_img:
#         return 'UR'
# #
# #
# b = cardlist[1:]
# dic = {}
# for _ in b:
#     for i in card_level:
#         if _+'.jpg' in i:
#             dic[_]= cardlevel(i)
# print(dic)
# print(len(dic))
# print(len(b))

# def house(i):
#     cur.execute(f'insert into house(id) value ({i})')
#     con.commit()
# #
# for i in range(2, 101):
#     house(i)

# time = datetime.datetime.now()+datetime.timedelta(days=+1)
# user_id = 1327960105
# print(time, type(time))

# cur.execute('select id from card')
# res = cur.fetchall()
# for i in res:
#     user_id = i[0]
#     cur.execute(f'select * from card where id = {user_id}')
#     res = cur.fetchone()[1:]
#     list = cardlist[1:]
#     sum_N = 0
#     sum_R = 0
#     for num, _ in enumerate(list):
#         if _ + '.jpg' in N_img:
#             sum_N += res[num]
#         if _ + '.jpg' in R_img:
#             sum_R += res[num]
#     gg('u', 'id', user_id, 'N', sum_N)
#     gg('u', 'id', user_id, 'R', sum_R)


achieve_list = {
    '全卡牌终极玩家': ['北极土豆', '林佳奇——通天龙王', '视角姬——银河系二王子', '陈扬——B站螃蟹', '林佳奇——吃素的狮子', '视角姬——无业游民', '陈扬——六道轮回', '林佳奇——百万调音师', '团子', '小仙若', '小初', '李彧', '桃核', '欠欠', '欣小萌', '泡芙喵', '漠漠——多情浪子', '漠漠——工具女', '碳酸熊卡', '蚀血之暗', '豆豆子', '醋醋', '陶宇杰', '韩小沐', 'Dio', '丧男', '伢伢', '妥妥', '小陈', '戢子丰', '李正雄', '曲一畅', '李荣民', '林汉业', '果哝双子', '王志达', '秋雾雾', '老菌菌', '萌爱moi', '萍萍', '西凉', '韩忠颖', '460缝合怪', 'coser丁', 'COSER丙', 'Coser乙', 'Coser甲', 'Dio的家', '东尼羞耻板', '乌龙', '二饼', '亮亮', '伪醋醋', '元宝', '动漫高手', '喜鹊', '实体娃娃A', '实体娃娃B', '小暗做的屎', '小暗的兔耳', '小暗的黑丝', '小狮子玩偶', '帝王蟹A', '帝王蟹B', '帝王蟹C', '帝王蟹D', '杨秘书', '油炸冰棍', '消防员', '火鸡', '狮子同学乙', '狮子同学甲', '狮子日记1', '狮子日记2', '狮子游泳圈', '狮子班主任', '狮子班长', '范助理', '被烤的火鸡', '视角姬的自恋照', '视角姬的黑丝', '视角姬车模乙', '豆豆子的胸垫', '车模丁', '车模丙', '车模甲', '鬼畜高手', '刘苏良', '朱一旦', '王瀚哲', '老番茄', '陈再强', 'A路人', '逗川', '小V', '欠欠——独立女仆长', '小潮院长', '海皇', '平守', '伊丽莎白鼠', '痒局长'],
    '终极460': ['林佳奇——通天龙王', '视角姬——银河系二王子', '陈扬——B站螃蟹', '林佳奇——吃素的狮子', '视角姬——无业游民', '陈扬——六道轮回'],
    '高级460': ['林佳奇——通天龙王', '视角姬——银河系二王子', '陈扬——B站螃蟹'],
    '中级460': ['林佳奇——吃素的狮子', '视角姬——无业游民', '陈扬——六道轮回'],
    '狮子CP团': ['林佳奇——吃素的狮子', '小仙若', '小初', '豆豆子', '醋醋', '欣小萌', ],
    '防道少女团': ['陈扬——六道轮回', '漠漠——工具女', '醋醋', '韩小沐', '伢伢', '妥妥',  '果哝双子',  '萍萍', ],
    '视角姬女仆团': ['视角姬——无业游民', '欠欠', '团子', '碳酸熊卡', '萌爱moi', ],
    # '女仆长': ['欠欠——独立女仆长'],
    '四大欠王': ['林佳奇——吃素的狮子', 'A路人', '伊丽莎白鼠', '痒局长'],
    '狮林国际': ['林佳奇——吃素的狮子', '陶宇杰', '曲一畅', '李荣民', '王志达', '秋雾雾', '老菌菌', '西凉', '韩忠颖', '李彧', ],
    '半壁江山': ['漠漠——工具女', '醋醋', '韩小沐', '伢伢', '妥妥',  '果哝双子',  '萍萍',  '小仙若', '小初', '豆豆子', '醋醋', '欣小萌', ],
    '0+7狂热者': ['林佳奇——吃素的狮子', '狮子同学乙', '狮子同学甲', '狮子日记1', '狮子日记2', '狮子游泳圈', '狮子班主任', '狮子班长', ],
    '小潮工作室': ['小潮院长', '海皇'],
    'coser爱好者': ['coser丁', 'COSER丙', 'Coser乙', 'Coser甲'],
    '车模爱好者': ['视角姬车模乙', '车模丁', '车模丙', '车模甲'],
    '帝王蟹爱好者': ['帝王蟹A', '帝王蟹B', '帝王蟹C', '帝王蟹D'],
    '萌宠爱好者': ['乌龙', '二饼', '元宝', '喜鹊', ],
    '猎奇控': ['小暗做的屎', '小暗的兔耳', '小暗的黑丝', '视角姬的自恋照', '视角姬的黑丝', '460缝合怪', '豆豆子的胸垫', ],
    '物品收集者': ['Dio的家', '东尼羞耻板', '伪醋醋', '动漫高手', '鬼畜高手', ],
}
cur.execute('select id from u')
user = cur.fetchall()

for i in user:
    ach = ''
    user_id = i[0]
    print(user_id)
    cur.execute(f'select * from card where id = {user_id}')
    res = cur.fetchone()
    card = {}
    print(res)
    if res:
        for i in range(1, len(res)):
            card[cardlist[i]] = res[i]
        for _ in achieve_list:
            nice = 1
            for i in achieve_list[_]:
                if card[i] == 0:
                    nice = 0
            if nice == 1:
                ach += _ + ' '
            else:
                nice = 1
    sql = f'update u set achievement="{ach}" where id = {user_id}'
    cur.execute(sql)
    con.commit()
    print(sql)
print(cardlist)