from .tool import *


@on_command('est', aliases=('开始投标',), permission=permission.SUPERUSER)
async def est(session: CommandSession):
    gg('con', 'id', 'est', 'con', 1)
    await session.send('开启成功')


@on_command('est1', aliases=('结束投标',), permission=permission.SUPERUSER)
async def est1(session: CommandSession):
    gg('con', 'id', 'off', 'con', 0)
    await session.send('已结束')


@on_command('off', aliases=('开始竞选',), permission=permission.SUPERUSER)
async def off(session: CommandSession):
    gg('con', 'id', 'off', 'con', 1)
    await session.send('开启成功')


@on_command('off1', aliases=('结束竞选',), permission=permission.SUPERUSER)
async def off1(session: CommandSession):
    gg('con', 'id', 'off', 'con', 0)
    await session.send('已结束')


def est_jx(user_id, txt):
    est, num = txt.split(' ')
    score = ye(user_id)
    num = int(num)
    est = int(est)
    if score < num or num < 5:
        return pa
    if not 0 < est < 6:
        return pa
    cur.execute(f'select owner from estate')
    res = cur.fetchall()
    for i in res:
        if i[0] == str(user_id):
            return '每人只可以投标一块土地哦~'
    cur.execute(f'select owner from official')
    res = cur.fetchall()
    for i in res:
        if i[0] == str(user_id):
            return '官员不可以当地主哦~'
    cur.execute(f'select * from estate where id = {est}')
    res = cur.fetchone()
    if res[2] == 0:
        kcjf(user_id, num)
        gg('estate', 'id', est, 'owner', user_id)
        gg('estate', 'id', est, 'price', num)
        return f'竞价成功,扣除积分{num}'
    if res[2] >= num:
        return f'目前最高价是{res[2]}'
    elif res[2] < num:
        zjjf(res[1], res[2])
        kcjf(user_id, num)
        gg('estate', 'id', est, 'owner', user_id)
        gg('estate', 'id', est, 'price', num)
        return f'竞价成功,扣除积分{num}'


def off_jx(user_id, txt):
    off, num = txt.split(' ')
    score = ye(user_id)
    num = int(num)
    off = int(off)
    if score < num or num < 10:
        return pa
    if not 0 < off < 4:
        return pa
    cur.execute(f'select owner from official')
    res = cur.fetchall()
    for i in res:
        if i[0] == str(user_id):
            return '每人只担任一个官职哦~'
    cur.execute(f'select owner from estate')
    res = cur.fetchall()
    for i in res:
        if i[0] == str(user_id):
            return '地主不可以当官哦~'
    cur.execute(f'select * from official where id = {off}')
    res = cur.fetchone()
    if res[2] == 0:
        kcjf(user_id, num)
        gg('official', 'id', off, 'owner', user_id)
        gg('official', 'id', off, 'price', num)
        return f'竞选成功,扣除积分{num}'
    if res[2] >= num:
        return f'目前最高价是{res[2]}'
    elif res[2] < num:
        zjjf(res[1], res[2])
        kcjf(user_id, num)
        gg('official', 'id', off, 'owner', user_id)
        gg('official', 'id', off, 'price', num)
        return f'竞选成功,扣除积分{num}'


@on_command('est_j', aliases=('#地产投标',), only_to_me=False)
async def est_j(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    cur.execute('select con from con where id = "est"')
    res = cur.fetchone()[0]
    house = select('u', 'rent', 'id', user_id)[0]
    if not res:
        return
    if not house:
        await session.send('没地方住的人无资格参与投标')
        return
    txt = session.get('txt', prompt='请输入想要竞价的土地编号：1-5，空格后标注价格，10分起拍。')
    str1 = est_jx(user_id, txt)
    await session.send(str1)


@on_command('off_j', aliases=('#官员竞选',), only_to_me=False)
async def off_j(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    cur.execute('select con from con where id = "off"')
    res = cur.fetchone()[0]
    house = select('u', 'rent', 'id', user_id)[0]
    if not res:
        return
    if not house:
        await session.send('没地方住的人无资格参与竞选')
        return
    txt = session.get('txt', prompt='请输入想要竞选的官员编号：1-3，空格后标注价格，15分起拍。')
    str1 = off_jx(user_id, txt)
    await session.send(str1)


@on_command('direction', aliases='#发展方向')
async def direc(session: CommandSession):
    group_id = session.ctx.group_id
    user_id = session.ctx['sender']['user_id']
    if not group_id:
        cur.execute('select con from con where id = "est"')
        res = cur.fetchone()[0]
        if res:
            await session.send('请等待竞价结束')
            return
        cur.execute(f'select * from estate where owner = {user_id}')
        res = cur.fetchone()
        if res[3] == 0:
            txt = session.get('txt', prompt=f'您的房产号：{res[0]}，可选择的发展方向有：1为制造业，2为农业，3为服务业'
                                            f'请输入序号1、2、3选择,仅可选择一次。')
            num = int(txt)
            if 0 < num < 4:
                gg('estate', 'id', res[0], 'direction', num)
                await session.send(f'选定成功，您的{res[0]}号地产已选定发展方向：{direction_dic[num]}。')

@on_command('direction_up', aliases='#up')
async def direc_up(session: CommandSession):
    group_id = session.ctx.group_id
    user_id = session.ctx['sender']['user_id']
    cur.execute('select con from con where id = "off"')
    res = cur.fetchone()[0]
    if res:
        await session.send('请等待竞选结束')
        return
    if not group_id:
        cur.execute('select con from con where id = "off"')
        res = cur.fetchone()[0]
        if res:
            await session.send('请等待竞选结束')
            return
        cur.execute(f'select * from official where owner = {user_id}')
        res = cur.fetchone()
        if res:
            txt = session.get('txt', prompt=f'可选择的up的发展方向有：1为制造业，2为农业，3为服务业请输入序号1、2、3选择。')
            num = int(txt)
            if 0 < num < 4:
                gg('official', 'id', res[0], 'up', num)
                await session.send(f'选定成功，您已选定up发展方向为{direction_dic[num]}，可随时更改。')

@on_command('direction_down', aliases='#down')
async def direc_down(session: CommandSession):
    group_id = session.ctx.group_id
    user_id = session.ctx['sender']['user_id']
    if not group_id:
        cur.execute('select con from con where id = "off"')
        res = cur.fetchone()[0]
        if res:
            await session.send('请等待竞选结束')
            return
        cur.execute(f'select * from official where owner = {user_id}')
        res = cur.fetchone()
        if res:
            txt = session.get('txt', prompt=f'可选择的down的发展方向有：1为制造业，2为农业，3为服务业请输入序号1、2、3选择。')
            num = int(txt)
            if 0 < num < 4:
                gg('official', 'id', res[0], 'down', num)
                await session.send(f'选定成功，您已选定down发展方向为{direction_dic[num]}，可随时更改。')


def invest_money(user_id, txt):
    num, money = txt.split(' ')
    score = ye(user_id)
    num = int(num)
    money = int(money)
    if score < money or not 0 < num < 6:
        return pa
    cur.execute(f'update u set investment={num},money=money+{money} where id ={user_id}')
    con.commit()
    kcjf(user_id, money)
    return f'投资成功，剩余积分{ye(user_id)}'


@on_command('invest', aliases='#投资', only_to_me=False)
async def invest(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    cur.execute(f'select owner from official')
    res = cur.fetchall()
    for i in res:
        if i[0] == str(user_id):
            return '官员不可参与投资~'
    cur.execute('select id, direction from estate')
    res = cur.fetchall()
    str1 = ''
    for i in res:
        str1 += f'{i[0]}号发展方向：{direction_dic[i[1]]}   '
    txt = session.get('txt', prompt=str1+'请输入想要投资的号码与积分，中间使用空格隔开。')
    str1 = invest_money(user_id, txt)
    await session.send(str1, at_sender=True)

@on_command('invest_1', aliases='#撤回投资', only_to_me=False)
async def invest_1(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    cur.execute(f'update u set investment=0, score=score+money,money=0 where id ={user_id}')
    con.commit()
    await session.send('撤回成功', at_sender=True)


@on_command('invest_2', aliases='#我的投资', only_to_me=False)
async def invest_2(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    cur.execute(f'select investment,money from u where id = {user_id}')
    u = cur.fetchone()
    str1 = f'你投资了{u[0]}号地产共{u[1]}积分'
    await session.send(str1, at_sender=True)


def up_num(off):
    up = [1, 1, 1]
    for i,num in enumerate(off):
        print(num)
        if num[4] != 0:
            up[num[4]-1] += 0.2
        if num[3] != 0:
            up[num[3]-1] -= 0.3
    print(up)
    return up

@on_command('account', aliases='#结算', permission=permission.SUPERUSER)
async def account(session: CommandSession):
    cur.execute('select * from estate')
    est = cur.fetchall()
    cur.execute('select * from official')
    off = cur.fetchall()
    cur.execute('select id,investment,money from u')
    u = cur.fetchall()
    up = up_num(off)
    # await session.send(f'{est}\n{off}\n{u}\n{up}')
    scores = [0, 0, 0, 0, 0, 0]
    for i in u:
        if i[1] != 0:
            score = int(i[2] * up[est[i[1]-1][3]-1]*0.9)
            cur.execute(f'update u set investment=0,money=0,score=score+{score} where id={i[0]}')
            con.commit()
            scores[est[i[1]-1][0]-1] += int(i[2] * up[est[i[1]-1][3]-1] * 0.1)
            await bot.send_msg(user_id=i[0], message=f'本次投资{i[1]}号地产收获连本带利共{score}')
    for i in est:
        cur.execute(f'update u set score=score+{scores[i[0]-1]} where id={i[1]}')
        await bot.send_msg(user_id=i[1], message=f'本次投资{i[1]}号地产收收获共{scores[i[0]-1]}')
        con.commit()
        cur.execute(f'update estate set direction=0 where id={i[0]}')
        con.commit()

@on_command('account_1', aliases='#结束了', permission=permission.SUPERUSER)
async def account_1(session: CommandSession):
    cur.execute('select * from estate')
    est = cur.fetchall()
    for i in est:
        await bot.send_msg(user_id=i[1], message=f'您投标的{i[0]}号地成功，请决定其发展方向：#发展方向')
    cur.execute('select * from official')
    off = cur.fetchall()
    for i in off:
        await bot.send_msg(user_id=i[1], message=f'您是{i[0]}号官员，可以决定扶持产业与打压产业了：#up和#down')


@on_command('account_2', aliases='#官员任务', permission=permission.SUPERUSER)
async def account_3(session: CommandSession):
    cur.execute('select * from official')
    off = cur.fetchall()
    for i in off:
        if i[3] == 0:
            await bot.send_msg(user_id=i[1], message=f'{i[0]}号官员，请尽快决定打压产业：#down')
        if i[4] == 0:
            await bot.send_msg(user_id=i[1], message=f'{i[0]}号官员，请尽快决定扶持产业：#up')

@on_command('account_3', aliases='#资产', only_to_me=False)
async def account_1(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    cur.execute('select * from estate')
    est = cur.fetchall()
    for i in est:
        if i[1] == user_id:
            await session.send(f'您拥有{i[0]}号地产', at_sender=True)
    cur.execute('select * from official')
    off = cur.fetchall()
    for i in off:
        if i[1] == user_id:
            await session.send(f'您是{i[0]}号官员', at_sender=True)
