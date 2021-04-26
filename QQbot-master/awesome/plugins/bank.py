from .tool import *


def loan_t(id):
    cur.execute(f'select * from bank where id={id}')
    res = cur.fetchone()
    a, loan, date = res[0], res[1], res[2]
    return loan, date


def deposit(id):
    cur.execute(f'select * from bank where id={id}')
    res = cur.fetchone()
    if res:
        return bank_21
    score = ye(id)
    if score >= 2:
        cur.execute(f'insert into bank(id) value({id}) ')
        con.commit()
        kcjf(id, 2)
        return bank_3
    else:
        return bank_20


def bank(id, num):
    if num > 100:
        return bank_1
    cur.execute(f'select * from bank where id={id}')
    res = cur.fetchone()
    if not res:
        return bank_19
    id, loan, date = res[0], res[1], res[2]
    if loan > 0:
        return bank_2
    else:
        t1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute(f'update bank set loan = {num},date1="{t1}" where id = {id}')
        con.commit()
        cur.execute(f'update u set score=score+{num} where id = {id}')
        con.commit()
        return bank_4


def interest(id):
    cur.execute(f'select * from bank where id={id}')
    res = cur.fetchone()
    id, loan, date = res[0], res[1], res[2]
    now = datetime.datetime.now()
    days = (now - date).days
    hours = int((now - date).seconds / 3600) + days * 24
    pays = int(loan * hours / 100)+1
    if loan == 0:
        pays = 0
    return pays, loan


def pay(id, num):
    cur.execute(f'select * from bank where id={id}')
    res = cur.fetchone()
    if not res:
        return bank_19
    id, loan, date = res[0], res[1], res[2]
    yes = ye(id)
    if num < 0:
        return '爬！'
    if yes < num:
        return bank_5
    if loan == 0:
        return
    else:
        pays, x = interest(id)
        money = pays+loan
    if num < pays:
        return bank_6
    else:
        if num < money:
            gg('bank', 'id', id, 'loan', money-num)
            cur.execute(f'update u set score=score-{num} where id = {id}')
            con.commit()
            t1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute(f'update bank set loan = {money-num},date1="{t1}" where id = {id}')
            con.commit()
            return bank_7(money, num)
        elif num >= money:
            gg('bank', 'id', id, 'loan', 0)
            cur.execute(f'update u set score=score-{money} where id = {id}')
            con.commit()
            return bank_8


@on_command('TT', aliases=('#交易积分', '#积分交易', '#转账', 'jf'), only_to_me=False)
async def searchscore(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    if day(user_id):
        await session.send('需要先签到的说~'+newgame, at_sender=True)
        return
    try:
        loan, ss = loan_t(user_id)
    except:
        loan = ''
    if loan:
        await session.send('先把欠的钱还了再想着转账吧！', at_sender=True)
        return
    txt = session.get('txt', prompt='请输入@要交易的人+积分\n')
    t1 = await jf(user_id, txt)
    await session.send(t1, at_sender=True)


async def jf(user_id, txt):
    cur.execute('select score from u where id = %s', user_id)
    res = cur.fetchone()[0]
    uv = 1
    x = txt.split(' ')
    id = nums(x[0])
    x[1] = int(nums(x[1]))
    if int(res) < int(x[1]):
        return '穷鬼爬！'
    if id == user_id:
        return '转你妈呢转！'
    if int(x[1]) <= 0:
        return '转账有这么转的？'
    cur.execute(f'select score from u where id = "{id}"')
    sc = cur.fetchone()[0]
    gg('u', 'id', user_id, 'score', int(res) - int(x[1]))
    jjj = int(int(x[1]*uv))
    gg('u', 'id', id, 'score', int(sc) + +jjj)
    return f'交易成功,{jjj}积分已到账'


async def ph():
    con = pymysql.connect(host='localhost', user='root', password='282610', database='qqbot', charset='utf8')
    cur = con.cursor()
    cur.execute(f'select id,score from u')
    s = cur.fetchall()
    dict = {}
    for i in s:
        dict[i[0]] = i[1]
    d = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    str1 = '   积分排行榜   \n'
    for i in range(10):
        str1 += f'第{i+1}名，[CQ:at,qq={d[i][0]}], 积分：{d[i][1]}\n'
    con.commit()
    return str1

async def grph(user_id):
    cur.execute(f'select id,score from u')
    s = cur.fetchall()
    dict = {}
    for i in s:
        dict[i[0]] = i[1]
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

def random_steal():
    a = random.randint(0, 100)
    if a < 30:
        return 1, '偷窃成功'
    elif a < 35:
        return 2, '偷窃被反杀'
    elif a <65:
        return 3, '偷窃被警察发现'
    else:
        return 4, '偷窃失败'

async def steal(user_id):
    cur.execute(f'select id from u where rent =0')
    res = cur.fetchall()
    a = random.randint(0, len(res)-1)
    id = res[a][0]
    score1 = ye(user_id)
    score2 = ye(id)
    num, str1 = random_steal()
    if score2 <4:
        return '对方是个穷光蛋呢......'
    if num == 1:
        score = int(score2*0.3)
        kcjf(id, score)
        zjjf(user_id, score)
        try:
            await bot.send_msg(user_id=id, message=f'你遭遇了小偷，损失{score}积分，温馨提示，您可能需要一个住房。')
        except:
            pass
        return f'{str1},获得{score}积分'
    elif num == 2:
        score = int(score1*0.3)
        kcjf(user_id, score)
        zjjf(id, score)
        await bot.send_msg(user_id=id, message=f'你遭遇了小偷，你反杀了他，获得{score}积分，温馨提示，您可能需要一个住房。')
        return f'{str1},损失{score}积分'
    elif num == 3:
        score = int(score1*0.3)
        kcjf(user_id, score)
        return f'{str1},罚款{score}积分'
    else:
        return str1


@on_command('grph1', aliases=('#财富排行', '#财富排名'), only_to_me=False)
async def grphb(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    phb = await grph(user_id)
    await session.send(phb, at_sender=True)

@on_command('bc', aliases=('#积分降临', 'bc'), permission=permission.SUPERUSER)
async def bc(session: CommandSession):
    txt = session.get('jl')
    x = txt.split(' ')
    id = nums(x[0])
    cur.execute('select score from u where id = %s', id)
    res = cur.fetchone()[0]
    res = int(res) + int(x[1])
    gg('u', 'id', id, 'score', res)
    await session.send(f'{x[1]}积分已到账。')


@on_command('kc', aliases=('#扣除降临', 'kc'), permission=permission.SUPERUSER)
async def bc(session: CommandSession):
    txt = session.get('jl')
    x = txt.split(' ')
    id = nums(x[0])
    kcjf(id, int(x[1]))
    await session.send(f'{x[1]}积分已扣除。')


@on_command('jc', aliases=('#检查积分', 'jc'), permission=permission.SUPERUSER)
async def jc(session: CommandSession):
    txt = session.get('jc')
    id = nums(txt)
    res = select('u', 'score', 'id', id)[0]
    await session.send(str(res), at_sender=True)


@on_command('bank1', aliases=('#借积分', 'jq'), only_to_me=False)
async def cha(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    if day(user_id):
        await session.send('需要先签到的说~'+newgame, at_sender=True)
        return
    jf = int(session.get('jf', prompt='请输入“想要借的积分数目”，最大可以借100。\n', at_sender=True))
    str1 = bank(user_id, jf)
    await session.send(str1, at_sender=True)

@on_command('banks', aliases=('#还积分', 'hq'), only_to_me=False)
async def cha(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    if day(user_id):
        await session.send('需要先签到的说~'+newgame, at_sender=True)
        return
    # await session.send(str(interest(user_id)))
    jf = int(session.get('jf', prompt='请输入“打算还的积分数目”。\n', at_sender=True))
    str1 = pay(user_id, jf)
    await session.send(str1, at_sender=True)

@on_command('pays', aliases=('#利息',), only_to_me=False)
async def cha(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    pays, loan = interest(user_id)
    str1 = f'当前欠款积分：{loan}\n利息：{pays}，总计待还：{loan+pays}'
    loan_t(user_id)
    await session.send(str1, at_sender=True)


@on_command('depo', aliases=('#开户',), only_to_me=False)
async def depo(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    if day(user_id):
        await session.send('需要先签到的说~'+newgame, at_sender=True)
        return
    jf = session.get('jf', prompt='开户需支付两积分，是否继续？1表示继续，其余表示不继续。\n', at_sender=True)
    if jf == '1':
        str1 = deposit(user_id)
        await session.send(str1, at_sender=True)
    else:
        return

@on_command('ph', aliases=('#积分排行榜', 'phb'), permission=permission.SUPERUSER)
async def scgm(session: CommandSession):
    phb = await ph()
    await session.send(phb)


# @on_command('steal_card', aliases=('#偷窃卡', ), only_to_me=False)
# async def steal_card(session: CommandSession):
#     user_id = session.ctx['sender']['user_id']
#     if day(user_id):
#         await session.send('需要先签到的说~'+newgame, at_sender=True)
#         return
#     times = datetime.datetime.now().hour
#     if not (times < 8 or times > 21):
#         await session.send('大白天的不太好吧？')
#         return
#     score = ye(user_id)
#     jf = session.get('jf', prompt='一张偷窃卡需要10积分，是否支付？1表示继续，其余表示不继续。\n', at_sender=True)
#     if jf == '1' and score >= 10:
#         kcjf(user_id, 10)
#         str1 = await steal(user_id)
#         await session.send(str1, at_sender=True)
#         return
#     else:
#         await session.send('穷鬼'+pa, at_sender=True)



# @on_command('cfcx', aliases=('#财富查询', '#财富', '#我的财富', 'cf'), only_to_me=False)
# async def cha(session: CommandSession):
#     user_id = str(session.ctx['sender']['user_id'])
#     str1 = await sec2(user_id)
#     sum1, sjj = await sj(user_id)
#     str1 += sum1
#     await session.send(str1, at_sender=True)


@on_command('bbc', aliases='#新赛季奖励', only_to_me=False)
async def bbc(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    cur.execute(f'select * from bc where id = {user_id}')
    res = cur.fetchone()
    if not res:
        cur.execute(f'insert into bc value ({user_id}, "1")')
        con.commit()
        zjjf(user_id, 500)
        await session.send('500积分已到账', at_sender=True)
    else:
        await session.send('给老子爬！', at_sender=True)
