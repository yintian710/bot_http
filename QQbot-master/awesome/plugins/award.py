from .tool import *

@on_command('#participate', aliases='#460', only_to_me=False)
async def ard(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    cur.execute(f'select user_id from awards where user_id = "{user_id}"')
    res = cur.fetchone()
    if res:
        await session.send(pa, at_sender=True)
    else:
        cur.execute(f'insert into awards(user_id) values("{user_id}")')
        con.commit()
        await session.send(f'参与成功，请等候开奖', at_sender=True)


@on_command('k_ard', aliases='#开奖', only_to_me=False)
async def k_ard(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    if user_id not in [1327960105, 942788328]:
        return
    cur.execute('select user_id from awards')
    res = cur.fetchall()
    num = len(res)
    user = res[random.randint(0, num-1)][0]
    await session.send(f'阿凯宠幸了[CQ:at,qq={user}]')


@on_command('num_ard', aliases='#参与人数', only_to_me=False)
async def k_ard(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    if user_id not in [1327960105, 942788328]:
        return
    cur.execute('select user_id from awards')
    res = cur.fetchall()
    num = len(res)
    await session.send(f'参与人数为{num}人')
