import pymysql
from nonebot import on_command, CommandSession
from awesome.plugins.tool import *


async def sj(user_id):
    cur.execute(f'select * from u where id = {user_id}')
    user = cur.fetchone()
    cur.execute(f'select gpdm,gpjg from cg')
    dic = cur.fetchall()
    jg = {}
    for i in dic:
        jg[i[0]]=i[1]
    data = {}
    sum = int(user[1])
    for i in range(3, len(user)-2):
        data[gp[i-3]] = (int(user[i]))
    for i in range(len(data)):
        sum += data[gp[i]]*jg[gp[i]]
    return f'身价共{sum}积分', sum

def js(sy, num, score, jg, user_id, gpdm, id):
    s = 0
    jg *= int(num)
    print(jg)
    score = select('u', 'score', 'id', user_id)  # 用户剩余积分
    gg('u', 'id', user_id, 'score', int(score) - jg)
    gg('jysc', 'id', id, 'num', int(sy) - int(num))
    if cz('u', gpdm):
        s = select('u', gpdm, 'id', user_id)
        gg('u', 'id', user_id, gpdm, int(s) + int(num))
        return f'购买成功，花费{jg}积分，当前{gpdm}股共{int(s) + int(num)}'
    else:
        print(gpdm)
        zj('u', gpdm, user_id)
        gg('u', 'id', user_id, gpdm, s + int(num))
        return f'购买成功，花费{jg}积分，当前{gpdm}股共{int(s) + int(num)}'

def js1(sy, num, score, jg, user_id, gpdm, id):
    score = int(score)
    jg = int(jg) * int(num)  # 所需要的价格
    s = select('u', gpdm, 'id', user_id)
    if cz('u', gpdm):
        if int(s) < int(num):
            return '穷鬼爬！'
        gg('u', 'id', user_id, gpdm, int(s) - int(num))
        gg('u', 'id', user_id, 'score', int(score) + jg)
        gg('jysc', 'id', id, 'num', int(sy) - int(num))
    else:
        return '求你去看一眼自己口袋！'

    return f'出售成功，获得{jg}积分，当前{gpdm}股共{int(s) - int(num)}'

def gg(base, id, user_id, x, y):  # 更改 x为需要更改的属性，y为改后的值
    sql = f"update {base} set {x}={y} where {id}='{user_id}'"
    cur.execute(sql)
    con.commit()

def select(base, x, a, b):
    cur.execute(f'select {x} from {base} where {a} = "{str(b)}"')
    res = (cur.fetchone()[0])
    if res is None:
        res = 0
    return res

def cz(table, col):  # 判断股票是否已经存在
    sql = f"select count(*) from information_schema.columns where table_name = '{table}' and column_name = '{col}'"
    cur.execute(sql)
    con.commit()
    if cur.fetchone()[0] == 0:
        return False
    else:
        return True

def zj(table, col, user_id):  # 增加个人股仓
    sql = f"alter table {table} add {col} varchar(20)"
    # print(sql)
    cur.execute(sql)
    gg(table, 'id', user_id, col, '0')
    con.commit()

def sti(x):  # str to int
    s = 0
    for i in x:
        if i != '(' and i != ')' and i != ',':
            s = s * 10 + int(i)
    return s

async def clean(id, user_id):
    id = int(id)
    cur.execute(f'select * from jysc where id = {id}')
    res = cur.fetchone()
    print(res)
    if res:
        if user_id == res[4]:
            if res[-1] == '0':
                gg('jysc', 'id', res[0], 'num', '0')
                dj(res[4])
                return '撤销成功!'
            if res[-1] == '1':
                cur.execute(f'select {res[1]} from u where id = {res[4]}')
                s = cur.fetchone()[0]
                gg('u', 'id', res[4], res[1], int(s) + int(res[3]))
                gg('jysc', 'id', res[0], 'num', '0')
                return '撤销成功!'
        else:
            return '动脑子想想这是不是你的订单！给爷爬！'
    else:
        return '订单号都输不对？给爷爬！'


async def buy(user_id, gpdm, num):
    score = select('u', 'score', 'id', user_id)  # 用户剩余积分
    score = int(score)
    dj = select('u', 'dj', 'id', user_id)
    print('1', gpdm)
    jg = select('cg', 'gpjg', 'gpdm', gpdm)
    # jg = cur.execute('select gpjg from cg where  gpdm= %s', gpdm)
    jg = int(jg) * int(num)  # 所需要的价格
    sy = select('cg', 'gpsy', 'gpdm', gpdm)
    print(score, jg, score - jg, sy)
    s = 0
    if int(num) <= 0:
        return pa
    if int(sy) < int(num):
        return '市场剩余股票不足'
    if int(score)-dj < int(jg):
        return f'撒泡尿照照钱包求你了！'
    gg('u', 'id', user_id, 'score', int(score) - jg)
    gg('cg', 'gpdm', gpdm, 'gpsy', int(sy) - int(num))
    if cz('u', gpdm):
        s = select('u', gpdm, 'id', user_id)
        gg('u', 'id', user_id, gpdm, int(s) + int(num))
        return f'购买成功，花费{jg}积分，当前{gpdm}股共{int(s) + int(num)},剩余积分{int(score) - jg}'
    else:
        zj('u', gpdm, user_id)
        gg('u', 'id', user_id, gpdm, s + int(num))
        return f'购买成功，花费{jg}积分，当前{gpdm}股共{int(s) + int(num)},剩余积分{int(score) - jg}'

# async def sell(user_id, gpdm, num):
# 	con = pymysql.connect(host='localhost', user='root', password='282610', database='qqbot', charset='utf8')
# 	cur = con.cursor()
# 	score = select('u', 'score', 'id', user_id)  # 用户剩余积分
# 	score = int(score)
# 	# print('1', gpdm)
# 	jg = select('cg', 'gpjg', 'gpdm', gpdm)
# 	# jg = cur.execute('select gpjg from cg where  gpdm= %s', gpdm)
# 	jg = int(jg) * int(num)  # 所需要的价格
# 	sy = select('cg', 'gpsy', 'gpdm', gpdm)
# 	if cz('u', gpdm):
# 		s = select('u', gpdm, 'id', user_id)
# 		if int(s) < int(num):
# 			return '您没有这么多的股票'
# 		gg('u', 'id', user_id, gpdm, int(s) - int(num))
# 		gg('u', 'id', user_id, 'score', int(score) + jg)
# 		gg('cg', 'gpdm', gpdm, 'gpsy', int(sy) + int(num))
# 	else:
# 		return '您没有这个股票哦~'
#
# 	return f'出售成功，获得{jg}积分，当前{gpdm}股共{int(s) - int(num)},剩余积分{int(score) + jg}'

async def scgp():  # 输出股票
    cur.execute('select gpm, gpdm, gpsy, gpjg from cg')
    x = cur.fetchall()
    # print(x)
    tr1 = '股票名   股票代码   市场剩余   股票价格\n'
    for i in x:
        for _ in i:
            tr1 = tr1 + str(_) + '  '
        tr1 += '\n'
    tr1 += '\n请输入‘股票代码 购买数量’\n'
    return tr1


async def sec1(sc, id):
    tr1 = '交易单号 股票代码 价格 剩余数量 订单所有者 买/卖\n'
    if sc == '0':
        # cur.execute(f'select * from jysc where num != "0"')
        # res = cur.fetchall()
        # for i in res:
        #     for _ in i:
        #         tr1 = tr1 + str(_) + '  '
        #     tr1 += '\n'
        # tr1 += '0表示购买，1表示出售'
        # return tr1
        pass
    elif sc == '1':
        cur.execute(f'select * from jysc where num != "0" and user_id ={id}')
        res = cur.fetchall()
        if not res:
            return '未找到订单'
        for i in res:
            for _ in i:
                tr1 = tr1 + str(_) + '  '
            tr1 += '\n'
        tr1 += '0表示购买，1表示出售'
        return tr1
    else:
        cur.execute(f'select * from jysc where num != "0" and gpdm ="{sc}"')
        res = cur.fetchall()
        if not res:
            return '未找到订单'
        for i in res:
            for _ in i:
                tr1 = tr1 + str(_) + '  '
            tr1 += '\n'
        tr1 += '0表示购买，1表示出售'
        return tr1

async def sec2(user_id):
    cur.execute(f'select * from u where id = {user_id}')
    res = cur.fetchone()
    str = f"积分：{res[1]}  持有股票：  \n{gp[0]}:{res[3]}, {gp[1]}:{res[4]}, {gp[2]}:{res[5]}, {gp[3]}:{res[6]}, " \
          f"{gp[4]}:{res[7]}, {gp[5]}:{res[8]}, {gp[6]}:{res[9]}, {gp[7]}:{res[10]}, {gp[8]}:{res[11]}\n"
    con.commit()
    return str

async def gpjy(user_id, gpdm, num, jg):
    num = int(num)
    jg = int(jg)
    score = select('u', 'score', 'id', user_id)  # 用户剩余积分
    dj1 = select('u', 'dj', 'id', user_id)  # 用户冻结积分
    score = int(score)
    if num <= 0:
        return pa
    if score - dj1 < jg*num:
        return f'穷鬼爬!'
    cur.execute(f'select * from jysc where gpdm = "{gpdm}" and sell = 1 and num != "0"')
    zs = cur.fetchall()
    print(zs)
    str1 = ''
    if zs:
        for _ in zs:
            s1 = int(select('u', 'score', 'id', _[4]))
            sum = int(select('u', gpdm, 'id', _[4]))
            if _[2] <= jg:
                if sti(_[3]) >= num:
                    if _[4] == user_id:
                        gg('u', 'id', _[4], gpdm, sum +num)
                        gg('jysc', 'id', _[0], 'num', int(_[3]) - int(num))
                        return str1 + '购买完毕'
                    score = int(select('u', 'score', 'id', user_id))  # 用户剩余积分
                    str1 += (js(_[3], num, score, _[2], user_id, gpdm, _[0])) + '\n'
                    gg('u', 'id', _[4], 'score', s1 + (_[2] * num))
                    return str1 + '购买完毕'
                else:
                    if _[4] == user_id:
                        gg('u', 'id', _[4], gpdm, sum + int(_[3]))
                        gg('jysc', 'id', _[0], 'num', 0)
                        num -= int(_[3])
                        continue
                    str1 += js(_[3], _[3], score, _[2], user_id, gpdm, _[0]) + '\n'
                    gg('u', 'id', _[4], 'score', s1 + (_[2] * int(_[3])))
                    score = int(select('u', 'score', 'id', user_id))  # 用户剩余积分
                    gg('u', 'id', _[4], gpdm, sum - int(_[3]))
                    # gg('u', 'id', user_id, 'score', score - (_[2] * num))
                    num -= int(_[3])
        sql = f'insert into jysc(gpdm, jg, num, sell, user_id) value ("{gpdm}", {jg}, "{num}", "0", "{user_id}")'
        cur.execute(sql)
        con.commit()
        dj(user_id)
        return str1 + '市场单数不足，已自动挂单'
    else:
        sql = f'insert into jysc(gpdm, jg, num, sell, user_id) value ("{gpdm}", {jg}, "{num}", "0", "{user_id}")'
        cur.execute(sql)
        con.commit()
        dj(user_id)
        return "市场未发现交易单，已自动挂单"

async def gpgd(user_id, gpdm, num, jg):
    num = int(num)
    jg = int(jg)
    score = select('u', 'score', 'id', user_id)  # 用户剩余积分
    score = int(score)
    cur.execute(f'select * from jysc where gpdm = "{gpdm}" and sell = 0 and num != "0"')
    zs = cur.fetchall()
    print(zs)
    sum1 = int(select('u', gpdm, 'id', user_id))
    s = select('u', gpdm, 'id', user_id)
    if num <= 0:
        return pa
    if int(s) < num:
        return '孩子，去看一眼钱包，不会的话“#玩法”教你。'
    if zs:
        for _ in zs:
            s1 = int(select('u', 'score', 'id', _[4]))
            sum = int(select('u', gpdm, 'id', _[4]))
            str1 = ''
            if _[2] >= jg:
                if sti(_[3]) >= num:
                    if _[4] == user_id:
                        gg('jysc', 'id', _[0], 'num', int(_[3])-num)
                        return str1 + '出售成功'
                    # 	return str1 + '购买完毕'
                    str1 += js1(_[3], num, score, _[2], user_id, gpdm, _[0]) + '\n'
                    gg('u', 'id', _[4], 'score', s1 - (_[2] * num))
                    gg('u', 'id', _[4], gpdm, sum + num)
                    dj(_[4])
                    return str1 + '出售成功'
                else:
                    if _[4] == user_id:
                        gg('jysc', 'id', _[0], 'num', 0)
                        num -= int(_[3])
                        continue
                    str1 += js1(_[3], _[3], score, _[2], user_id, gpdm, _[0]) + '\n'
                    gg('u', 'id', _[4], 'score', s1 - (_[2] * int(_[3])))
                    gg('u', 'id', _[4], gpdm, sum + int(_[3]))
                    num -= int(_[3])
                    dj(_[4])
        gg('u', 'id', user_id, gpdm, sum1 - num)
        sql = f'insert into jysc(gpdm, jg, num, sell, user_id) value ("{gpdm}", {jg}, "{num}", "1", "{user_id}")'
        cur.execute(sql)
        con.commit()
        return str1 + '挂单成功'
    else:
        gg('u', 'id', user_id, gpdm, sum1 - num)
        sql = f'insert into jysc(gpdm, jg, num, sell, user_id) value ("{gpdm}", {jg}, "{num}", "1", "{user_id}")'
        cur.execute(sql)
        con.commit()
        return '已创建交易单'

async def ph():
    con = pymysql.connect(host='localhost', user='root', password='282610', database='qqbot', charset='utf8')
    cur = con.cursor()
    cur.execute(f'select id,score from u')
    s = cur.fetchall()
    dict = {}
    for i in s:
        str, sj_num = await sj(i[0])
        dict[i[0]] = sj_num
    d = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    str1 = '   身价排行榜   \n'
    for i in range(10):
        # print(d[i], end='  ')
        str1 += f'第{i+1}名，[CQ:at,qq={d[i][0]}],身价：{d[i][1]}\n'
    print(str1)
    con.commit()
    return str1

async def grph(user_id):
    cur.execute(f'select id,score from u')
    s = cur.fetchall()
    dict = {}
    for i in s:
        str, sj_num = await sj(i[0])
        dict[i[0]] = sj_num
    d = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    con.commit()
    for i, j in enumerate(d, start=1):
        if j[0] == user_id:
            if i == 1:
                s1 = '首富牛逼！\n'
            elif i <= 10:
                s1 = '前十大佬，惹不起惹不起。\n'
            elif i >50:
                s1 = '其实我不是很想搭理穷鬼...\n'
            else:
                s1 = ''
            return s1 + f'排名：{i}\n身价：{j[1]}\n'


# @on_command('grph', aliases=('#财富排行', '#财富排名', 'grph'), only_to_me=False)
# async def grphb(session: CommandSession):
#     user_id = str(session.ctx['sender']['user_id'])
#     phb = await grph(user_id)
#     await session.send(phb, at_sender=True)
#     # await session.send('功能暂时下架')


async def jc(gp, num, jg):
    cur.execute(f"update cg set gpzs=gpzs+{num},gpsy=gpsy+{num},gpjg={jg} where gpdm='{gp}'")
    con.commit()
    return '加仓成功'

@on_command('gpjc', aliases='加仓', permission=permission.SUPERUSER)
async def gpjc(session: CommandSession):
    txt = session.get('txt',prompt=await scgp())
    gp, num, jg = txt.split(' ')
    str1 = await jc(gp, num, jg)
    await session.send(str1, at_sender=True)

if __name__ == '__main__':
    # gpjy('1327960105', 'htl27', '10', '13')
    # gpgd('1873611947', 'xxr', '100', '6')
    dj('1327960105')
    # ph()
    pass
