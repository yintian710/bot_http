import random
import time

import aiocqhttp

from .tool import *

dic = {}
flag = True
flag1 = False
horses = ["π©", "π¦", "π»", "π", "π°", 'π']
# horses = ["πΆ", "π¨", "π©", "π΄", "π΅π°"]
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


# @on_command('start', aliases=('#ζ―θ΅εΌε§', '#θ΅ι©¬εΌε§', 'ζ―θ΅εΌε§', 'εΌε§ζ―θ΅'), permission=permission.SUPERUSER)
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
#         await session.send('εδΈδΊΊζ°οΌ'+ str(players) + '\nεδΈη§―εοΌ' + str(sums))
#         while judge():
#             for i in range(5):
#                 dis[i] -= int(random.randint(1, 5)*speed[i])
#             s = showhorse()
#             await session.send(f'{s}')
#             await asyncio.sleep(5)
#         # winner = 5
#         await session.send(f'ζ­ε{winner}ε·θ·εΎθε©!')
#         users = [k for k, v in dic.items() if v == winner]
#         for i in users:
#             print(num[i])
#             cur.execute("update u set score=score+'{}' where id = '{}'".format(int(num[i] * odds[winner-1]), i))
#             con.commit()
#             await session.send(f'ζ­ε[CQ:at,qq={i}] θ·εΎ{int(num[i]*odds[winner-1])}η§―ε')
#     cur.close()
#     con.close()
#     num = {}
#     dic = {}

@on_command('start', aliases=('#ζ―θ΅εΌε§', '#θ΅ι©¬εΌε§', 'ζ―θ΅εΌε§', 'εΌε§ζ―θ΅'), permission=permission.SUPERUSER)
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
            await session.send('εδΈδΊΊζ°οΌ' + str(players) + '\nεδΈη§―εοΌ' + str(sum1))
        except:
            pass
        while judge():
            for i in range(6):
                dis[i] -= int(random.randint(0, 5)*speed[i])
            s = showhorse()
            await session.send(f'{s}')
            await asyncio.sleep(15)
        # winner = 5
        await session.send(f'ζ­ε{winner}ε·θ·εΎθε©!')
        dic = {}
        num = {}
        try:
            for i in res:
                dic[i[0]] = i[2]
                num[i[0]] = i[1]
        except:
            await session.send('εΌε₯ε€±θ΄₯')
            return
        users = [k for k, v in dic.items() if v == winner]
        for i in users:
            print(num[i])
            cur.execute("update u set score=score+'{}' where id = '{}'".format(int(num[i] * odds[winner-1]), i))
            con.commit()
            await session.send(f'ζ­ε[CQ:at,qq={i}] θ·εΎ{int(num[i]*odds[winner-1])}η§―ε')
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
        str13 = f'ζ­ε{winner}ε·θ·εΎθε©!'
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
            win.append(f'ζ­ε[CQ:at,qq={i}] θ·εΎ{int(num[i]*odds[winner-1])}η§―ε')
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
        return 'ε?ιεοΌ50εδ»₯δΈζιε«ζ’­εοΌ'
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
        return f'ζ’­εζε,θ·εΎδΏεΊεεγ'


def wdxz(user_id):
    flag1 = horse_t()
    if not flag1:
        return 'ε―οΌη¬οΌ'
    cur.execute(f'select * from xz where id = {user_id}')
    res = cur.fetchone()
    if res:
        return f'δΈζ³¨ιζοΌ{horses[res[2]-1]}\nδΈζ³¨η§―εοΌ{res[1]}'
    else:
        return 'η¬'


async def smxz(user_id, s, nums):
    flag1 = horse_t()
    if not flag1:
        return 'ε―οΌη¬οΌ'
    nums = int(nums)
    if nums <= 0:
        return 'η¬οΌ'
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
                return "ζ²‘η§―εηη»η·η¬οΌ"
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
            return f'δΈζ³¨ζε,ζ£ι€η§―ε{temp}'


@on_command('horse', aliases=('#η«ι', 'η«ι'), permission=permission.SUPERUSER)
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
    strodds = so + '\nε»Ίθ??ζθδΈδΈοΌη°ε?δΈ­θ―·εΏθ΅εγ'
    await session.send(f'θΎε₯β#δΈζ³¨βε³ε―δΈζ³¨γ\nζ¬εΊθ΅ηδΈΊ\n'+strodds+'\n'
        f'δΈε―ζΌζ³¨δΈ€εΉι©¬οΌε¦εεδΈζ¬‘ζΌζ³¨ε°δΌεζΆοΌη§―εδΈθΏθΏγ\n'
        f'ε―ιε€ζΌζ³¨οΌε³ε ζ³¨γ\n'
        f'ηΊ―ε±ε¨±δΉοΌη°ε?δΈ­θ―·εΏθ΅εγ\n')

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
    strodds = so + '\nε»Ίθ??ζθδΈδΈοΌη°ε?δΈ­θ―·εΏθ΅εγ'
    str2 = (f'θΎε₯β#δΈζ³¨βε³ε―δΈζ³¨γ\nζ¬εΊθ΅ηδΈΊ\n'+strodds+'\n'
        f'δΈε―ζΌζ³¨δΈ€εΉι©¬οΌε¦εεδΈζ¬‘ζΌζ³¨ε°δΌεζΆοΌη§―εδΈθΏθΏγ\n'
        f'ε―ιε€ζΌζ³¨οΌε³ε ζ³¨γ\n'
        f'ηΊ―ε±ε¨±δΉοΌη°ε?δΈ­θ―·εΏθ΅εγ\n')
    return str1, str2


@on_command('xz', aliases=('#δΈζ³¨', 'xz'), only_to_me=False)
async def cxgp(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    if day(user_id):
        await session.send('ιθ¦εη­Ύε°ηθ―΄~'+newgame, at_sender=True)
        return
    flag1 = horse_t()
    odds = sodds()
    so = ''
    for i in range(6):
        so +=str(horses[i])+'1:'+str(odds[i])+'  '
    strodds = so+'\nε»Ίθ??ζθδΈδΈοΌη°ε?δΈ­θ―·εΏθ΅εγ'
    if flag1:
        xz = session.get('xz', prompt=f'θ―·θΎε₯βι©¬ηηΌε· δΈζ³¨η§―εβοΌζ¬εΊθ΅η:\n'+strodds, at_sender=True)
        ma, num = xz.split(' ')
        x = await smxz(user_id, ma, num)
        await session.send(x, at_sender=True)
    else:
        await session.send('ε―οΌη¬οΌ', at_sender=True)


@on_command('cxxz', aliases=('#ζ₯θ―’δΈζ³¨',), only_to_me=False)
async def cxxz(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    xz = wdxz(user_id)
    await session.send(xz, at_sender=True)


@on_command('sh', aliases=('#ζ’­ε',), only_to_me=False)
async def sh(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    if day(user_id):
        await session.send('ιθ¦εη­Ύε°ηθ―΄~'+newgame, at_sender=True)
        return
    flag1 = horse_t()
    odds = sodds()
    so = ''
    for i in range(6):
        so += str(horses[i]) + '1:' + str(odds[i]) + '  '
    strodds = so + '\nε»Ίθ??ζθδΈδΈοΌη°ε?δΈ­θ―·εΏθ΅εγ'
    if flag1:
        ma = session.get('xz', prompt=f'θ―·ι?ζ¨θ¦ζ’­εθ°οΌζ¬εΊθ΅η:\n'+strodds, at_sender=True)
        str1 = await smsh(user_id, ma)
        await session.send(str1, at_sender=True)
    else:
        await session.send('ε―οΌη¬οΌ', at_sender=True)


@on_command('horse1', aliases=('#θ΅ι©¬', 'θ΅ι©¬'), permission=permission.SUPERUSER)
async def horse(session: CommandSession):
    await session.send('δ½ ζ―δΈζ―ζ³θ―΄βcpη«ιβοΌ')


@on_command('cal', aliases='#24ηΉ', only_to_me=False)
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
    await session.send('θΏδΈͺεθ½ζζΆε³ι­δΊε¦~')


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
    data = []  # ζ°ζ?ζ 
    opt = []  # ζδ½η¬¦ζ 
    i = 0  # θ‘¨θΎΎεΌιεη΄’εΌ
    while i < len(s):
        if s[i].isdigit():  # ζ°ε­οΌε₯ζ data
            start = i  # ζ°ε­ε­η¬¦εΌε§δ½η½?
            while i + 1 < len(s) and s[i + 1].isdigit():
                i += 1
            data.append(int(s[start: i + 1]))  # iδΈΊζεδΈδΈͺζ°ε­ε­η¬¦ηδ½η½?
        elif s[i] == ")":  # ε³ζ¬ε·οΌoptεΊζ εζΆdataεΊζ εΉΆθ?‘η?οΌθ?‘η?η»ζε₯ζ dataοΌη΄ε°optεΊζ δΈδΈͺε·¦ζ¬ε·
            while opt[-1] != "(":
                process(data, opt)
            opt.pop()  # εΊζ "("
        elif not opt or opt[-1] == "(":  # ζδ½η¬¦ζ δΈΊη©ΊοΌζθζδ½η¬¦ζ ι‘ΆδΈΊε·¦ζ¬ε·οΌζδ½η¬¦η΄ζ₯ε₯ζ opt
            opt.append(s[i])
        elif s[i] == "(" or compare(s[i], opt[-1]):  # ε½εζδ½η¬¦δΈΊε·¦ζ¬ε·ζθζ―ζ ι‘Άζδ½η¬¦δΌεηΊ§ι«οΌζδ½η¬¦η΄ζ₯ε₯ζ opt
            opt.append(s[i])
        else:  # δΌεηΊ§δΈζ―ζ ι‘Άζδ½η¬¦ι«ζΆοΌoptεΊζ εζΆdataεΊζ εΉΆθ?‘η?οΌθ?‘η?η»ζε¦ζ data
            while opt and not compare(s[i], opt[-1]):
                if opt[-1] == "(":  # θ₯ιε°ε·¦ζ¬ε·οΌεζ­’θ?‘η?
                    break
                process(data, opt)
            opt.append(s[i])
        i += 1  # ιεη΄’εΌεη§»
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
#             await bot.send(ctx, "δ½ ζδΈͺε±")
#             return
#         s = calculate(s)
#         if s == 24:
#             await bot.send(ctx, f"ζ­εθ§£ε³,θ·εΎ{a}η§―ε")
#             con = pymysql.connect(host='localhost', user='root', password='282610', database='qqbot', charset='utf8')
#             cur = con.cursor()
#             user_id = str(ctx['sender']['user_id'])
#             cur.execute(f"update u set score=score+{a} where id = '{user_id}'")
#             con.commit()
#             cur.close()
#             con.close()


@on_command('mme', aliases=('#ι©¬εΏ', 'me'), only_to_me=False)
async def mme(session: CommandSession):
    h = ''
    for i in horses:
        h += i + '  '
    await session.send(h, at_sender=True)


@on_command('qb', aliases=('#δΈζ³¨ζζ₯', 'qb'), permission=permission.SUPERUSER)
async def qb(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    sum = [0, 0, 0, 0, 0, 0]
    jff = [0, 0, 0, 0, 0, 0]
    str1 = ''
    for i in range(1, 7):
        cur.execute(f'select jf from xz where ma={i}')
        res1 = cur.fetchall()
        cur.execute(f'select {i}ε· from con where id = "odds"')
        res2 = cur.fetchone()[0]
        for j in res1:
            sum[i-1] += j[0]
            jff[i-1] = res2
        # print(sum1)
    for i, _ in enumerate(sum):
        str1 += f'{horses[i]}δΈζ³¨η§―ε:{_}\n'
    await session.send(str1)



