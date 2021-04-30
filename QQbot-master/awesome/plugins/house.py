from .tool import *

def rent_house(user_id, txt):
    house, days = txt.split(' ')
    price = house_price * int(days)
    score = ye(user_id)
    if not 0 < int(house) <= 100:
        return pa
    if score < price:
        return pa
    res = select('house', 'tenants1', 'id', house)[0]
    if res != '0':
        return '你选的房子已经被人租去啦！'
    gg('house', 'id', house, 'tenants1', user_id)
    kcjf(user_id, price)
    gg('u', 'id', user_id, 'rent', house)
    t1 = (datetime.datetime.now()+datetime.timedelta(days=+int(days))).strftime("%Y-%m-%d")
    print(type(t1))
    cur.execute(f'update u set rent_time="{t1}" where id = {user_id}')
    con.commit()
    return f'花费{price}，租到了{house}号房子。'


def rent_again(user_id, txt, house):
    days = int(txt)
    price = house_price * int(days)
    score = ye(user_id)
    if score < price:
        return pa
    time = select('u', 'rent_time', 'id', user_id)[0]
    t1 = (time+datetime.timedelta(days=+int(days))).strftime("%Y-%m-%d")
    cur.execute(f'update u set rent_time="{t1}" where id = {user_id}')
    con.commit()
    kcjf(user_id, price)
    return f'花费{price}，续租{house}号房子。'


@on_command('house', aliases='#租房', only_to_me=False)
async def house(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    res = select('u', 'rent', 'id', user_id)[0]
    str1 = '你已经有房子住了。'
    if res == 0:
        txt = session.get('txt', prompt=f'请输入要租住的门牌号（1-100）空格+天数，{house_price}积分一天。')
        str1 = rent_house(user_id, txt)
        await session.send(str1, at_sender=True)
    else:
        await session.send(str1, at_sender=True)


@on_command('rent_again', aliases='#续租', only_to_me=False)
async def rentagain(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    res = select('u', 'rent', 'id', user_id)[0]
    str1 = '你哪来的房子住？'
    if res != 0:
        txt = session.get('txt', prompt=f'请输入要续租的天数，{house_price}积分一天。')
        str1 = rent_again(user_id, txt, res)
        await session.send(str1, at_sender=True)
    else:
        await session.send(str1, at_sender=True)


@on_command('null_house', aliases='#空房子', only_to_me=False)
async def null_house(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    cur.execute('select * from house')
    res = cur.fetchall()
    str1 = ''
    for i in res:
        if i[1] == '0' and i[2] == '0':
            str1 += f'{i[0]}   '
    await bot.send_msg(user_id=user_id, message=str1)

@on_command('my_house', aliases=('#我的住所', '#房子'), only_to_me=False)
async def null_house(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    cur.execute(f'select rent, rent_time from u where id = {user_id}')
    res = cur.fetchone()
    str1 = f'门牌号：{res[0]}，到期日期{res[1].strftime("%Y-%m-%d")}'
    await session.send(str1)
