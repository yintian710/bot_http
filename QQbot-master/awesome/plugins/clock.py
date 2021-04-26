from aiocqhttp.exceptions import Error as CQHttpError
from lose.cg import ph
from .horse import *
from .ticket import *

cs = 718348254

cp = 702052462

art = [['20', '14', '30']]
brt = [['20', '14', '40']]

def time():
    times = datetime.datetime.now().hour
    week = datetime.datetime.now().weekday()
    if times == 18 and week not in (5, 6):
    # if 1:
        print(times)
        return False
    else:
        print(times)
        return False


@nonebot.scheduler.scheduled_job('cron', hour='0', minute='0', second='10')
async def _():
    
    times = datetime.datetime.now()+datetime.timedelta(days=+1)
    cur.execute('delete from game')
    con.commit()
    cur.execute('select rent, rent_time,id from u')
    res = cur.fetchall()
    for i in res:
        if i[0] != 0:
            if times > i[1]:
                gg('u', 'id', i[2], 'rent', 0)
                gg('u', 'id', i[2], 'rent_time', 0)
                gg('house', 'id', i[0], 'tenants1', '0')
                await bot.send_msg(user_id=i[2], message=f'您的{i[0]}号房子到期了哦。')
            elif times == i[1]:
                await bot.send_msg(user_id=i[2], message=f'您的{i[0]}号房子即将到期了哦。')


@nonebot.scheduler.scheduled_job('cron', hour='10,13,17,22', minute='20', second='0')
async def _():
    bot = nonebot.get_bot()
    try:
        str1, str2 = await horse1()
        await bot.send_group_msg(group_id=cp,
                                 message=str1)
        await bot.send_group_msg(group_id=cp,
                                 message=str2)
        await bot.send_group_msg(group_id=cp,
                                 message='二十分钟后比赛开始，冲一冲搏一搏单车变摩托！发家致富别墅靠海！\n')
    except CQHttpError:
        pass


@nonebot.scheduler.scheduled_job('cron', hour='10,13,17,22', minute='40', second='0')
async def _():
    try:
        await qb()
    except:
        pass
    bot = nonebot.get_bot()
    st, str13, win, plays, sums = start1()
    if plays == 0:
        try:
            await bot.send_group_msg(group_id=cp,
                                     message='哎，终究是过了气， 跑马都没人跑了，告辞！')
        except:
            pass
        return
    try:
        await bot.send_group_msg(group_id=cp,
                                 message='参与人数：' + str(plays) + '\n参与积分：' + str(sums))
    except:
        pass
    try:
        if st:
            for _ in st:
                await bot.send_group_msg(group_id=cp,
                                         message=_)
                await asyncio.sleep(10)
        await bot.send_group_msg(group_id=cp,
                                 message=str13)
        if win:
            for _ in win:
                await bot.send_group_msg(group_id=cp,
                                         message=_)
        await bot.send_group_msg(group_id=cp,
                                 message=await ph())
    except CQHttpError:
        await bot.send_group_msg(group_id=cp,
                                 message='出错了哦2')
        pass


# @nonebot.scheduler.scheduled_job('cron', hour='*', minute='0', second='0')
# async def _():
#     # await bot.send_group_msg(group_id=cs, message=f'[CQ:record,file=file:///'
#     #                                               f'C:\\Users\\Administrator\\Desktop\\bot\\data\\voices\\{datetime.datetime.now().hour}.amr]')
#     await bot.send_group_msg(group_id=cp, message=f'[CQ:record,file=file:///'
#                                                   f'C:\\Users\\Administrator\\Desktop\\bot\\data\\voices\\{datetime.datetime.now().hour}.amr]')


@nonebot.scheduler.scheduled_job('cron', hour='0', minute='0', second='30')
async def _():
    x = random.randint(0, 100)
    if x < 50:
        a = 0
    elif x < 60:
        a = 1
    elif x < 70:
        a = 2
    elif x < 80:
        a = 3
    elif x < 85:
        a = 4
    else:
        a = 5
    await bot.send_msg(group_id=cp, message='[CQ:at, qq=all] 今天发生了：' + things[a])
    cur.execute('select id,score,rent from u')
    res = cur.fetchall()
    if a == 1:
        for i in res:
            if i[2] == 0:
                kcjf(i[0], 15)
    elif a == 2:
        for i in res:
            if i[2] == 0:
                kcjf(i[0], int(i[1]*0.25+1))
    elif a == 3:
        for i in res:
            if i[2] != 0:
                zjjf(i[0], 10)
    elif a == 4:
        for i in res:
            if i[2] == 0:
                kcjf(i[0], 10)
            elif i[2] != 0:
                gg('u', 'id', i[0], 'rent', 0)
                gg('u', 'id', i[0], 'rent_time', 0)
                gg('house', 'id', i[2], 'tenants1', '0')
                await bot.send_msg(user_id=i[0], message=f'您的{i[2]}号房子被地震摧毁了。')
    elif a == 5:
        for i in res:
            if i[2] == 0:
                await bot.set_group_ban(
                    group_id=702052462, user_id=i[0], duration=30
                )


@nonebot.scheduler.scheduled_job('cron', hour='*', minute='0', second='7')
async def _():
    cur.execute('select id from u')
    user = cur.fetchall()
    for i in user:
        ach = ''
        user_id = i[0]
        cur.execute(f'select * from card where id = {user_id}')
        res = cur.fetchone()
        card = {}
        if res:
            for i in range(1, len(res)):
                card[cardlist[i]] = res[i]
            for _ in achieve_list:
                nice = 1
                for i in achieve_list[_]:
                    if card[i] == 0:
                        nice = 0
                if nice == 1:
                    ach += _ + ' '
                else:
                    nice = 1
        sql = f'update u set achievement="{ach}" where id = {user_id}'
        cur.execute(sql)
        con.commit()

# @nonebot.scheduler.scheduled_job('cron', day_of_week='mon-fri', hour='18')
# async def _():
#     bot = nonebot.get_bot()
#     try:
#         await bot.send_group_msg(group_id=cp,
#                                  message='股市开盘啦！')
#         await bot.send_group_msg(group_id=cp,
#                                  message=await ph())
#     except CQHttpError:
#         pass


# @nonebot.scheduler.scheduled_job('cron', day_of_week='mon-fri', hour='17', minute='30')
# async def _():
#     bot = nonebot.get_bot()
#     try:
#         await bot.send_group_msg(group_id=cp,
#                                  message=await ph())
#         await bot.send_group_msg(group_id=cp,
#                                  message='距离开盘还有半小时')
#     except CQHttpError:
#         pass


# @nonebot.scheduler.scheduled_job('cron', day_of_week='mon-fri', hour='19', minute='0')
# async def _():
#     bot = nonebot.get_bot()
#     try:
#         await bot.send_group_msg(group_id=cp,
#                                  message='股市封盘啦~')
#         await bot.send_group_msg(group_id=cp,
#                                  message=await ph())
#     except CQHttpError:
#         pass


# @nonebot.scheduler.scheduled_job('cron', day_of_week='sun', hour='17', minute='58', second='0')
# async def _():
#     bot = nonebot.get_bot()
#     try:
#         await bot.send_group_msg(group_id=cp,
#                                  message='还有两分钟运气王开奖，各位可私聊我“我的运气王”查看自己购买过的运气王')
#     except:
#         pass


# @nonebot.scheduler.scheduled_job('cron', day_of_week='sun', hour='18', minute='0', second='0')
# async def _():
#     bot = nonebot.get_bot()
#     a, play, term = await kj1()
#     n = 20
#     cs = cp
#     try:
#         await bot.send_group_msg(group_id=cs,
#                                  message='运气王开启中......')
#         await asyncio.sleep(n)
#         await bot.send_group_msg(group_id=cs,
#                                  message=f'第四个号码为：{a[3]}')
#         await asyncio.sleep(n)
#         await bot.send_group_msg(group_id=cs,
#                                  message=f'第三个号码为：{a[2]}')
#         await asyncio.sleep(n)
#         await bot.send_group_msg(group_id=cs,
#                                  message=f'第二个号码为：{a[1]}')
#         await asyncio.sleep(n)
#         await bot.send_group_msg(group_id=cs,
#                                  message=f'关键号码为：{a[0]}')
#         await asyncio.sleep(n)
#         await bot.send_group_msg(group_id=cs,
#                                  message=f"一等奖为:{a}")
#         await asyncio.sleep(n)
#         for i in term:
#             play = await pjdr(a, i)
#         await bot.send_group_msg(group_id=cs,
#                                  message=f'一等奖中奖人次：{play[0]}\n'
#                                          f'二等奖中奖人次：{play[1]}\n'
#                                          f'三等奖中奖人次：{play[2]}\n'
#                                          f'安慰奖中奖人次：{play[3]}')
#     except:
#         pass



    # for i in res:
    #     if i[-1] == '0':
    #         gg('jysc', 'id', i[0], 'num', '0')
    #         dj(i[4])
    #     if i[-1] == '1':
    #         cur.execute(f'select {i[1]} from u where id = {i[4]}')
    #         s = cur.fetchone()[0]
    #         gg('u', 'id', i[4], i[1], int(s)+int(i[3]))
    #         gg('jysc', 'id', i[0], 'num', '0')


# @nonebot.scheduler.scheduled_job('cron', hour=art[0][0], minute=art[0][1], second=art[0][2])
# @nonebot.scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=3, minute='9', second=20)
# async def _():
#     bot = nonebot.get_bot()
#     try:
#         str1, str2 = await horse1()
#         await bot.send_group_msg(group_id=cs,
#                                  message=str1)
#         await bot.send_group_msg(group_id=cs,
#                                  message=str2)
#         await bot.send_group_msg(group_id=cs,
#                                  message='二十分钟后比赛开始，冲一冲搏一搏单车变摩托！发家致富别墅靠海！\n')
#     except CQHttpError:
#         pass
#
#
# @nonebot.scheduler.scheduled_job('cron', hour=brt[0][0], minute=brt[0][1], second=brt[0][2])
# async def _():
#     bot = nonebot.get_bot()
#     st, str13, win, plays, sums = start1()
#     try:
#         await bot.send_group_msg(group_id=cs,
#                                  message='参与人数：' + str(plays) + '\n参与积分：' + str(sums))
#     except:
#         pass
#     try:
#         if st:
#             for _ in st:
#                 await bot.send_group_msg(group_id=cs,
#                                          message=_)
#                 await asyncio.sleep(1)
#         await bot.send_group_msg(group_id=cs,
#                                  message=str13)
#         if win:
#             for _ in win:
#                 await bot.send_group_msg(group_id=cs,
#                                          message=_)
#     except CQHttpError:
#         await bot.send_group_msg(group_id=cp,
#                                  message='出错了哦2')
#         pass

