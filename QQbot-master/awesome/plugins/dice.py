from .tool import *


def dice_t():
    cur.execute('select con from con where id = "dice"')
    res = cur.fetchone()[0]
    if res == 1:
        return True
    else:
        return False


@on_command('dice', aliases='#骰子游戏', only_to_me=False)
async def dice(session: CommandSession):
    user_id = session.ctx['sender']['user_id']

    if dice_t():
        await session.send(dice_1)
    else:
        cur.execute('update con set con=1 where id = "dice"')
        con.commit()
        await session.send(dice_2)

@on_command('dice_play', aliases='#骰子', only_to_me=False)
async def dice_play(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    score = ye(user_id)
    if score < 10:
        await session.send(pa, at_sender=True)
        return
    # kcjf(user_id, 10)
    # txt = str(session.get('txt', prompt='请发送一个骰子。'))
    # nums = int(re.sub('\D', '', txt))
    await session.send(r'[CQ:dice]')
    # await session.send('1')
