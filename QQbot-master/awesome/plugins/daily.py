from .tool import *


def nums(x):
    global st
    num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(len(num)):
        num[i] = str(num[i])
    st = ''
    for i in x:
        if i in num:
            st += i
        # print(i)
    return st


def sti(x):  #str to int
    s = 0
    if x is None:
        return s
    for i in x:
        if i != '(' and i != ')' and i != ',' and i !="'":
            s = s * 10 + int(i)
    return s


@on_command('search_score', aliases=('#积分查询', '#查询积分', '#w我的积分'), only_to_me=False)
async def search(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    cur.execute('select score from u where id = %s', user_id)
    res = str(cur.fetchone())
    s = sti(res)
    if s:
        await session.send(f'{s}', at_sender=True)
        return
    await session.send(f'穷鬼爬！！', at_sender=True)


@on_command('djj', aliases=('#查询冻结', '#冻结积分'), only_to_me=False)
async def dj(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    cur.execute('select dj from u where id = %s', user_id)
    res = str(cur.fetchone())
    s = 0
    s = sti(res)
    if s:
        await session.send(f'{s}', at_sender=True)
    else:
        await session.send('您没有积分被冻结~')


@on_command('daily', aliases=('#签到', '#欧非鉴定术！', '#非欧鉴定术！', '#欧非鉴定术', '#非欧鉴定术', 'daily'), only_to_me=False)
async def daily(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    a = int((random.randint(20, 44)))
    if a <= 24:
        str2 = '不会真有人觉得自己签个到就能欧皇吧？不会吧不会吧？\n非酋签个到也才'
    elif a >= 41:
        str2 = '欧皇ohhh!!\n签到居然有'
    else:
        str2 = '...\n获得:'
    # a = 1000
    sss = 'select * from u where id = %s' % user_id
    sss = cur.execute(sss)
    print(sss)
    if sss == 0:
        cur.execute(f'insert into u(id) value ({user_id})')
        con.commit()
    sql = 'select score from u where id = %s' % user_id
    cur.execute(sql)
    n = str(cur.fetchone())
    score = sti(n)
    str1 = ''
    # if score >= 500:
    #     a = int(a*0.1)
    #     str1 = '\n积分超过五百，签到积分减少90%，'
    # elif score >= 400:
    #     a = int(a*0.6)
    #     str1 = '\n积分超过四百，签到积分减少60%,'
    # elif score >= 300:
    #     a = int(a*0.5)
    #     str1 = '\n积分超过三百，签到积分减少50%,'
    # elif score >= 200:
    #     a = int(a*0.6)
    #     str1 = '\n积分超过二百，签到积分减少40%,'
    a += score
    today = str(datetime.date.today())
    if not day(user_id):
        await session.send('臭不要脸签两次的爬！'+newgame, at_sender=True)
    else:
        s = "insert into u(id,score,da) values('{}','{}','{}') on DUPLICATE key update score='{}',da='{}'".\
            format(user_id, a, today, a, today)
        cur.execute(s)
        con.commit()
        await session.send(str2 + f'{a-score}积分！总积分:{a},'+str1+newgame, at_sender=True)


@on_command('aside', aliases=('#闲置积分', '闲置'), permission=permission.SUPERUSER)
async def daily(session: CommandSession):
    cur.execute('select score from u')
    res = cur.fetchall()
    sum1 = 0
    for i in res:
        sum1 += int(i[0])
    await session.send(f'闲置积分为：{sum1}')


@on_command('rumor', aliases=('#每日造谣', "#今日造谣"), only_to_me=False)
async def rumor(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    score = ye(user_id)
    try:
        res1 = select('game', 'id', 'id', user_id)[0]
    except:
        res1 = ''
    try:
        res = select('game', 'rumor', 'id', user_id)[0]
    except:
        res = []
    if not res1:
        cur.execute(f'insert into game(id, boom) value ({user_id}, 0)')
    if score < 5:
        await session.send(pa)
    if res:
        await session.send('造过谣的给爷爬！')
        return
    else:
        t = session.get('txt', prompt='请输入造谣内容，仅一次机会,且需要花费5积分,继续请先输入1再空格输入谣言，其他视为放弃。')
        a, txt = t.split(' ')
        if a != '1':
            return
        if 'image' in txt:
            await session.send('目前不支持图片造谣。')
            return
        gg('game', 'id', user_id, 'rumor', txt)
        kcjf(user_id, 5)
        await session.send('造谣成功。')

def rumor_list():
    cur.execute('select id, rumor from game')
    res = cur.fetchall()
    dic1 = {}
    dic2 = {}
    str1 = ''
    if res and res[0][0]:
        for num, _ in enumerate(res, start=1):
            if _[1]:
                dic1[num] = _[0]
                dic2[num] = _[1]
                str1 += f'\n{num}、{_[1][:int(len(_[1])/2)]}...'
    return dic1, dic2, str1


@on_command('look_rumor', aliases=('#查看谣言', '#今日谣言'), only_to_me=False)
async def look_rumor(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    score = ye(user_id)
    if score < 2:
        await session.send(pa, at_sender=True)
        return
    dic1, dic2, str1 = rumor_list()
    num = int(session.get('txt', prompt='今日谣言如下，查看一则谣言需要2积分，请输入谣言编号'+str1))
    try:
        await bot.send_msg(user_id=user_id, message=dic2[num])
        kcjf(user_id, 2)
        zjjf(dic1[num], 1)
    except:
        await session.send(pa)

@bot.on_message()
async def _(ctx: Context_T):
    message = str(ctx['message'])
    user_id = str(ctx['user_id'])
    if '群签到' in message:
        print(1)
        # return IntentCommand(90.0, 'daily')
