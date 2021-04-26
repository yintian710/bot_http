import aiocqhttp
from .tool import *
import time

play = [0, 0, 0, 0]
od = [35, 150, 888, 5]

async def pjdr(a, i):
    global play
    user_id = i[1]
    score = ye(user_id)
    num = i[3]
    tic = i[2]
    b = []
    for j in a+tic:
        b.append(j)
    res = 0
    comfort = False
    if b[0] == b[4]:
        comfort = True
        for k in (1, 2, 3):
            if b[k] == b[k+4]:
                res += 1
    if res == 0:
        if comfort:
            await bot.send_msg(user_id=user_id, message=f'您购买的{num}支{tic}中了安慰奖，获得{num*od[3]}积分。')
            gg('u', 'id', user_id, 'score', score+num*od[3])
            cur.execute(f'delete from ticket where id = "{i[0]}"')
            play[3] += num
        else:
            await bot.send_msg(user_id=user_id, message=f'您购买的{num}支{tic}未中奖，请再接再厉。')
            cur.execute(f'delete from ticket where id = "{i[0]}"')
    elif res == 1:
        await bot.send_msg(user_id=user_id, message=f'您购买的{num}支{tic}中了三等奖，获得积分{num*od[0]}。')
        gg('u', 'id', user_id, 'score', score+num*od[0])
        cur.execute(f'delete from ticket where id = "{i[0]}"')
        play[2] += num
    elif res == 2:
        await bot.send_msg(user_id=user_id, message=f'您购买的{num}支{tic}中了二等奖，获得积分{num*od[1]}。')
        gg('u', 'id', user_id, 'score', score+num*od[1])
        cur.execute(f'delete from ticket where id = "{i[0]}"')
        play[1] += num
    elif res == 3:
        await bot.send_msg(user_id=user_id, message=f'您购买的{num}支{tic}中了一等奖，获得积分{num*od[2]}。')
        gg('u', 'id', user_id, 'score', score+num*od[2])
        cur.execute(f'delete from ticket where id = "{i[0]}"')
        play[0] += num
    con.commit()
    return play


@on_command('tic', aliases=('#运气王', ), only_to_me=False)
async def tic(session: CommandSession):
    # user_id = str(session.ctx['sender']['user_id'])
    # if day(user_id):
    #     await session.send('需要先签到的说~'+newgame, at_sender=True)
    #     return
    # t = session.get('t', prompt=f'请输入一个四位数0-9999，空位使用0补齐，空格后输入购买数量，两分一支，可重复购买。\n', at_sender=True)
    # tic, num = t.split(' ')
    # try:
    #     str1 = buy_tic(user_id, tic, num)
    # except:
    #     await session.send('输错了！这都输不对？爬！')
    #     return
    str1 = '当前并未开始哦'
    await session.send(str1, at_sender=True)


@on_command('tick', aliases=('#福彩', ), only_to_me=False)
async def tic(session: CommandSession):
    await session.send('你想说的是不是“#运气王”？')


def buy_tic(user_id, tic, num):
    num = int(num)
    score = ye(user_id)
    if len(tic) != 4:
        return '四位数！不会数数还是咋地！'
    if score < num*2:
        return '使用#积分查询 可查询积分，去用用吧，不然真就不知道自己还有多少积分了？'
    gg('u', 'id', user_id, 'score', score-num*2)
    cur.execute(f"insert into ticket(user_id,tic,num) values('{user_id}','{tic}',{num})")
    con.commit()
    return f'购买{num}支{tic}成功，花费{num*2}积分。'


@on_command('kj', aliases=('#运气王开奖', 'kj'), permission=permission.SUPERUSER)
async def kj(session: CommandSession):
    global play
    con = pymysql.connect(host='localhost', user='root', password='282610', database='qqbot', charset='utf8')
    cur = con.cursor()
    a = str(random.randint(0, 9999))
    # a = '9602'
    n1 = 20
    while len(a) < 4:
        a = '0' + a
    cur.execute('select * from ticket')
    term = cur.fetchall()
    await session.send('运气王开启中......')
    await asyncio.sleep(n1)
    await session.send(f'第四个号码为：{a[3]}')
    await asyncio.sleep(n1)
    await session.send(f'第三个号码为：{a[2]}')
    await asyncio.sleep(n1)
    await session.send(f'第二个号码为：{a[1]}')
    await asyncio.sleep(n1)
    await session.send(f'关键号码为：{a[0]}')
    await asyncio.sleep(n1)
    await session.send(f"一等奖为:{a}")
    await asyncio.sleep(n1)
    for i in term:
        play = await pjdr(a, i)
    await session.send(f'一等奖中奖人次：{play[0]}\n'
                       f'二等奖中奖人次：{play[1]}\n'
                       f'三等奖中奖人次：{play[2]}\n'
                       f'安慰奖中奖人次：{play[3]}')
    play = [0, 0, 0]
    # cur.execute(f"delete from ticket")
    # con.commit()

async def kj1():
    global play
    con = pymysql.connect(host='localhost', user='root', password='282610', database='qqbot', charset='utf8')
    cur = con.cursor()
    a = str(random.randint(0, 9999))
    # if a in ['712', '419', '620', '265', '520', '521']:
    #     a = str(random.randint(0, 999))
    while len(a) < 4:
        a = '0' + a
    cur.execute('select * from ticket')
    term = cur.fetchall()
    play = [0, 0, 0]
    # cur.execute(f"delete from ticket")
    # con.commit()
    return a, play, term

@on_command('wdfc', aliases=('#我的气运', '#我的运气王', '#我的运气'), only_to_me=False)
async def wdfc(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    cur.execute(f'select * from ticket where user_id={user_id}')
    res = cur.fetchall()
    str1 = ''
    for i in res:
        str1 += f'\n号码{i[2]},数量：{i[3]}'
    await session.send(str1, at_sender=True)
