import random
import time

import aiocqhttp

from .tool import *

dic = {}
flag = True
flag1 = False
horses = ["🐩", "🦄", "🐻", "🐖", "🐰", '🐈']
# horses = ["👶", "👨", "👩", "👴", "👵🐰"]
discon = [30, 30, 30, 30, 30, 30]
dis = discon.copy()
speed = [1.4, 1.2, 1.6, 2, 2.2, 0.2]
num = {}
winner = 0
def showhorse():
    s = ""
    for i in range(0, 6):
        s += str(i + 1) + '|' + dis[i] * ' ' + horses[i]
        if i < 5:
            s += '\n'
    return s


def judge():
    temp = []
    global winner
    win = True
    for i in range(6):
        if dis[i] <= 0:
            temp.append(i + 1)
            win = False
    if len(temp):
        a = random.randint(0, int(len(temp) - 1))
        winner = temp[a]
    return win


# @on_command('start', aliases=('#比赛开始', '#赛马开始', '比赛开始', '开始比赛'), permission=permission.SUPERUSER)
# async def start(session: CommandSession):
#     global flag
#     global flag1
#     global num, dic
#     speed = sspeed()
#     odds = sodds()
#     flag = False
#     con = pymysql.connect(host='localhost', user='root', password='282610', database='qqbot', charset='utf8')
#     cur = con.cursor()
#     if flag1:
#         flag1 = False
#         flag = True
#         players = len(num)
#         sums = 0
#         try:
#             for i in num:
#                 sums += num[i]
#         except:
#             pass
#         await session.send('参与人数：'+ str(players) + '\n参与积分：' + str(sums))
#         while judge():
#             for i in range(5):
#                 dis[i] -= int(random.randint(1, 5)*speed[i])
#             s = showhorse()
#             await session.send(f'{s}')
#             await asyncio.sleep(5)
#         # winner = 5
#         await session.send(f'恭喜{winner}号获得胜利!')
#         users = [k for k, v in dic.items() if v == winner]
#         for i in users:
#             print(num[i])
#             cur.execute("update u set score=score+'{}' where id = '{}'".format(int(num[i] * odds[winner-1]), i))
#             con.commit()
#             await session.send(f'恭喜[CQ:at,qq={i}] 获得{int(num[i]*odds[winner-1])}积分')
#     cur.close()
#     con.close()
#     num = {}
#     dic = {}

@on_command('start', aliases=('#比赛开始', '#赛马开始', '比赛开始', '开始比赛'), permission=permission.SUPERUSER)
async def start(session: CommandSession):
    global flag
    global flag1
    global num, dic
    speed = sspeed()
    odds = sodds()
    flag = False
    flag1 = horse_t()
    cur.execute(f'select * from xz')
    res = cur.fetchall()
    await session.send(res)
    if flag1:
        flag1 = False
        flag = True
        try:
            players = len(res)
            sum1 = 0
            for _ in res:
                sum1 += _[1]
            await session.send('参与人数：' + str(players) + '\n参与积分：' + str(sum1))
        except:
            pass
        while judge():
            for i in range(6):
                dis[i] -= int(random.randint(0, 5)*speed[i])
            s = showhorse()
            await session.send(f'{s}')
            await asyncio.sleep(15)
        # winner = 5
        await session.send(f'恭喜{winner}号获得胜利!')
        dic = {}
        num = {}
        try:
            for i in res:
                dic[i[0]] = i[2]
                num[i[0]] = i[1]
        except:
            await session.send('开奖失败')
            return
        users = [k for k, v in dic.items() if v == winner]
        for i in users:
            print(num[i])
            cur.execute("update u set score=score+'{}' where id = '{}'".format(int(num[i] * odds[winner-1]), i))
            con.commit()
            await session.send(f'恭喜[CQ:at,qq={i}] 获得{int(num[i]*odds[winner-1])}积分')
    num = {}
    dic = {}
    horse_set(0)
    cur.execute('delete from xz')
    con.commit()


def start1():
    global flag, str13, win, players, num, dic
    global flag1
    global winner
    speed = sspeed()
    odds = sodds()
    flag = False
    flag1 = horse_t()
    cur.execute(f'select * from xz')
    res = cur.fetchall()
    st = []
    if flag1:
        flag1 = False
        flag = True
        players = len(num)
        try:
            players = len(res)
            sum1 = 0
            for _ in res:
                sum1 += _[1]
        except:
            return
        while judge():
            for i in range(6):
                dis[i] -= int(random.randint(0, 5)*speed[i])
            s = showhorse()
            st.append(f'{s}')
        # winner = 5
        str13 = f'恭喜{winner}号获得胜利!'
        dic = {}
        num = {}
        try:
            for i in res:
                dic[i[0]] = i[2]
                num[i[0]] = i[1]
        except:
            return
        users = [k for k, v in dic.items() if v == winner]
        win = []
        for i in users:
            print(num[i])
            cur.execute("update u set score=score+'{}' where id = '{}'".format(int(num[i] * odds[winner-1]), i))
            con.commit()
            win.append(f'恭喜[CQ:at,qq={i}] 获得{int(num[i]*odds[winner-1])}积分')
    cur.execute('delete from xz')
    con.commit()
    num = {}
    dic = {}
    sum1 = 0
    # print(type(st), type(str13), type(win))
    horse_set(0)
    return st, str13, win, players, sum1


bot = nonebot.get_bot()
nums = []

async def smsh(user_id, ma):
    score = ye(user_id)
    if score < 50:
        return '宁配吗？50分以上才配叫梭哈！'
    else:
        xwzu(user_id, ma, score)
        # print(select('xz', 'ma,jf', 'id', user_id))
        if not (user_id in dic):
            dic[user_id] = ma
            num[user_id] = score
        elif dic[user_id] != s:
            dic[user_id] = ma
            num[user_id] = score
        else:
            num[user_id] += score
        cur.execute(f"update u set score=10 where id = '{user_id}'")
        con.commit()
        return f'梭哈成功,获得保底十分。'


def wdxz(user_id):
    flag1 = horse_t()
    if not flag1:
        return '嗯？爬！'
    cur.execute(f'select * from xz where id = {user_id}')
    res = cur.fetchone()
    if res:
        return f'下注选手：{horses[res[2]-1]}\n下注积分：{res[1]}'
    else:
        return '爬'


async def smxz(user_id, s, nums):
    flag1 = horse_t()
    if not flag1:
        return '嗯？爬！'
    nums = int(nums)
    if nums <= 0:
        return '爬！'
    if s.isdigit() and int(s) in range(1, 7):
        if flag:
            s = int(s)
            print(s)
            cur.execute('select score from u where id = %s', user_id)
            res = cur.fetchone()
            con.commit()
            res = int(res[0])
            temp = int(nums)
            if res < temp:
                return "没积分的给爷爬！"
            xwzu(user_id, s, nums)
            # print(select('xz', 'ma,jf', 'id', user_id))
            if not (user_id in dic):
                dic[user_id] = s
                num[user_id] = nums
            elif dic[user_id] != s:
                dic[user_id] = s
                num[user_id] = nums
            else:
                num[user_id] += nums
            cur.execute("update u set score=score-'{}' where id = '{}'".format(temp, user_id))
            con.commit()
            return f'下注成功,扣除积分{temp}'


@on_command('horse', aliases=('#竞速', '竞速'), permission=permission.SUPERUSER)
async def horse(session: CommandSession):
    global flag1
    global dis
    sgg()
    speed = sspeed()
    odds = sodds()
    horse_set(1)
    dis = discon.copy()
    s = ""
    for i in num:
        num[i] = 1
    for i in dic:
        dic[i] = 0
    for i in range(0, 6):
        s += str(i+1) + '|' + dis[i]*' ' + horses[i]
        if i < 5:
            s += '\n'
    await session.send(f'{s}')
    so = ''
    for i in range(6):
        so += str(horses[i]) + '1:' + str(odds[i]) + '  '
    strodds = so + '\n建议思考一下，现实中请勿赌博。'
    await session.send(f'输入‘#下注’即可下注。\n本场赔率为\n'+strodds+'\n'
        f'不可押注两匹马，否则前一次押注将会取消，积分不返还。\n'
        f'可重复押注，即加注。\n'
        f'纯属娱乐，现实中请勿赌博。\n')

async def horse1():
    global flag1
    global dis
    sgg()
    speed = sspeed()
    odds = sodds()
    flag1 = True
    horse_set(1)
    dis = discon.copy()
    s = ""
    for i in num:
        num[i] = 1
    for i in dic:
        dic[i] = 0
    for i in range(0, 6):
        s += str(i+1) + '|' + dis[i]*' ' + horses[i]
        if i < 5:
            s += '\n'
    str1 = f'{s}'
    so = ''
    for i in range(6):
        so += str(horses[i]) + '1:' + str(odds[i]) + '  '
    strodds = so + '\n建议思考一下，现实中请勿赌博。'
    str2 = (f'输入‘#下注’即可下注。\n本场赔率为\n'+strodds+'\n'
        f'不可押注两匹马，否则前一次押注将会取消，积分不返还。\n'
        f'可重复押注，即加注。\n'
        f'纯属娱乐，现实中请勿赌博。\n')
    return str1, str2


@on_command('xz', aliases=('#下注', 'xz'), only_to_me=False)
async def cxgp(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    if day(user_id):
        await session.send('需要先签到的说~'+newgame, at_sender=True)
        return
    flag1 = horse_t()
    odds = sodds()
    so = ''
    for i in range(6):
        so +=str(horses[i])+'1:'+str(odds[i])+'  '
    strodds = so+'\n建议思考一下，现实中请勿赌博。'
    if flag1:
        xz = session.get('xz', prompt=f'请输入“马的编号 下注积分”，本场赔率:\n'+strodds, at_sender=True)
        ma, num = xz.split(' ')
        x = await smxz(user_id, ma, num)
        await session.send(x, at_sender=True)
    else:
        await session.send('嗯？爬！', at_sender=True)


@on_command('cxxz', aliases=('#查询下注',), only_to_me=False)
async def cxxz(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    xz = wdxz(user_id)
    await session.send(xz, at_sender=True)


@on_command('sh', aliases=('#梭哈',), only_to_me=False)
async def sh(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    if day(user_id):
        await session.send('需要先签到的说~'+newgame, at_sender=True)
        return
    flag1 = horse_t()
    odds = sodds()
    so = ''
    for i in range(6):
        so += str(horses[i]) + '1:' + str(odds[i]) + '  '
    strodds = so + '\n建议思考一下，现实中请勿赌博。'
    if flag1:
        ma = session.get('xz', prompt=f'请问您要梭哈谁？本场赔率:\n'+strodds, at_sender=True)
        str1 = await smsh(user_id, ma)
        await session.send(str1, at_sender=True)
    else:
        await session.send('嗯？爬！', at_sender=True)


@on_command('horse1', aliases=('#赛马', '赛马'), permission=permission.SUPERUSER)
async def horse(session: CommandSession):
    await session.send('你是不是想说“cp竞速”？')


@on_command('cal', aliases='#24点', only_to_me=False)
async def cal(session: CommandSession):
    # nums.clear()
    # a = random.randint(1, 10)
    # nums.append(a)
    # b = random.randint(1, 10)
    # nums.append(b)
    # c = random.randint(1, 10)
    # nums.append(c)
    # d = random.randint(1, 10)
    # nums.append(d)
    # nums.sort()
    # await session.send(f'{a} {b} {c} {d}')
    await session.send('这个功能暂时关闭了哦~')


def compare(op1, op2):
    return op1 in ["*", "/"] and op2 in ["+", "-"]


def getvalue(num1, num2, operator):
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "*":
        return num1 * num2
    else:
        return num1 / num2


def process(data, opt):
    operator = opt.pop()
    num2 = data.pop()
    num1 = data.pop()
    data.append(getvalue(num1, num2, operator))


def calculate(s):
    data = []  # 数据栈
    opt = []  # 操作符栈
    i = 0  # 表达式遍历索引
    while i < len(s):
        if s[i].isdigit():  # 数字，入栈data
            start = i  # 数字字符开始位置
            while i + 1 < len(s) and s[i + 1].isdigit():
                i += 1
            data.append(int(s[start: i + 1]))  # i为最后一个数字字符的位置
        elif s[i] == ")":  # 右括号，opt出栈同时data出栈并计算，计算结果入栈data，直到opt出栈一个左括号
            while opt[-1] != "(":
                process(data, opt)
            opt.pop()  # 出栈"("
        elif not opt or opt[-1] == "(":  # 操作符栈为空，或者操作符栈顶为左括号，操作符直接入栈opt
            opt.append(s[i])
        elif s[i] == "(" or compare(s[i], opt[-1]):  # 当前操作符为左括号或者比栈顶操作符优先级高，操作符直接入栈opt
            opt.append(s[i])
        else:  # 优先级不比栈顶操作符高时，opt出栈同时data出栈并计算，计算结果如栈data
            while opt and not compare(s[i], opt[-1]):
                if opt[-1] == "(":  # 若遇到左括号，停止计算
                    break
                process(data, opt)
            opt.append(s[i])
        i += 1  # 遍历索引后移
    while opt:
        process(data, opt)
    return data.pop()


# @bot.on_message('group')
# async def group_msg(ctx: Context_T):
#     s = str(ctx['message'])
#     n = len(s)
#     a = random.randint(1, 5)
#     if re.match("\(?\d{1,2}\)?[+\-*/]\(?\d{1,2}\)?[+\-*/]\(?\d{1,2}\)?[+\-*/]\(?\d{1,2}\)?", s):
#         flag2 = False
#         whole = []
#         i = 0
#         while i < n:
#             if s[i].isdigit():
#                 if i + 1 < n and s[i+1].isdigit():
#                     whole.append(10)
#                     i += 1
#                 else:
#                     whole.append(int(s[i]))
#             i += 1
#         whole.sort()
#         print(whole)
#         print(nums)
#         if not nums == whole:
#             await bot.send(ctx, "你搞个屁")
#             return
#         s = calculate(s)
#         if s == 24:
#             await bot.send(ctx, f"恭喜解决,获得{a}积分")
#             con = pymysql.connect(host='localhost', user='root', password='282610', database='qqbot', charset='utf8')
#             cur = con.cursor()
#             user_id = str(ctx['sender']['user_id'])
#             cur.execute(f"update u set score=score+{a} where id = '{user_id}'")
#             con.commit()
#             cur.close()
#             con.close()


@on_command('mme', aliases=('#马儿', 'me'), only_to_me=False)
async def mme(session: CommandSession):
    h = ''
    for i in horses:
        h += i + '  '
    await session.send(h, at_sender=True)


@on_command('qb', aliases=('#下注情报', 'qb'), permission=permission.SUPERUSER)
async def qb(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    sum = [0, 0, 0, 0, 0, 0]
    jff = [0, 0, 0, 0, 0, 0]
    str1 = ''
    for i in range(1, 7):
        cur.execute(f'select jf from xz where ma={i}')
        res1 = cur.fetchall()
        cur.execute(f'select {i}号 from con where id = "odds"')
        res2 = cur.fetchone()[0]
        for j in res1:
            sum[i-1] += j[0]
            jff[i-1] = res2
        # print(sum1)
    for i, _ in enumerate(sum):
        str1 += f'{horses[i]}下注积分:{_}\n'
    await session.send(str1)



