
from .tool import *


def min():
    cur.execute(f'select con from con where id = "min"')
    s = cur.fetchone()[0]
    if s == 1:
        return True
    else:
        return False

def maxnum():
    cur.execute(f'select * from mins')
    res = cur.fetchall()
    dic = {}
    dic1 = {}
    x = 0
    id = ''
    str1 = '参与情况：\n'
    for i in range(1, 21):
        dic1[21 - i] = 0
    for _ in res:
        dic[_[0]] = _[1]
    for j in dic:
        dic1[dic[j]] += 1
    for n in range(1, 21):
        if dic1[21 - n] == 1:
            x = 21-n
            break
    for k in dic:
        if dic[k] == x:
            id = k
    for l in dic1:
        if dic1[l] != 0:
            str1 = str1 + '参与积分：' + str(l) + '，参与数量：' +str(dic1[l]) + '\n'
    return id, x, str1, dic


async def news(dic, num):
    for i in dic.items():
        str1 = f'#猜猜谁最大 已开奖，获胜数字为：{num}'
        if i[1] == num:
            str1 = f'恭喜你获得本次#猜猜谁最大 的胜利。'
        await bot.send_msg(user_id=i[0], message=str1)


@on_command('min', aliases=('#最大数', 'zd'), permission=permission.SUPERUSER)
async def min1(session: CommandSession):
    if min():
        await session.send('比赛已经开始了，私聊我“#最大 参与积分”即可参加游戏。')
    else:
        gg('con', 'id', 'min', 'con', 1)
        await session.send('比赛开启成功，私聊我“#最大 参与积分”即可参加游戏。')


@on_command('minn', aliases=('#猜猜谁最大',), only_to_me=False)
async def minn(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    if min():
        await session.send('比赛已经开始了，私聊我“#最大 参与积分”即可参加游戏。')
        str1 = '发送“#最大 参与积分”即可参加游戏，参与积分最高20。\n举例：游戏获胜者为本轮游戏最大且唯一的数字，' \
               '若有相同的数字则出局。比方说这一局，参赛为：“20、20、19、19、17、16、15、15”，则17获胜。\n' \
               '自己的参赛积分记得保密哦~也不要相信别人告诉你的参赛积分哦~\n最高可获得下注积分平方倍奖励！'
        await bot.send_msg(user_id=user_id, message=str1)
    else:
        await session.send('游戏还未开始哦~')


@on_command('max1', aliases=('谁是最大？', 'd'), permission=permission.SUPERUSER)
async def max1(session: CommandSession):
    if not min():
        gg('con', 'id', 'min', 'con', 1)
        await session.send('比赛开启成功，私聊我“#最大 参与积分”即可参加游戏。')
    else:
        user_id, num, s1, dic = maxnum()
        await session.send(s1)
        await session.send(f'赢家为：[CQ:at,qq={user_id}]，他的数字为：{num}, 获得积分{num*10}')
        zjjf(user_id, num*10)
        gg('con', 'id', 'min', 'con', 0)
        delete('mins')
        await news(dic, num)

@on_command('max12', aliases=('#谁最大', 'szd'), permission=permission.SUPERUSER)
async def max12(session: CommandSession):
    if not min():
        gg('con', 'id', 'min', 'con', 1)
        await session.send('比赛开启成功，私聊我“#最大 参与积分”即可参加游戏。')
    else:
        user_id, num, s1, dic = maxnum()
        if len(dic) < 20:
            await session.send(f'参与人数不足，游戏暂不开始，目前人数：{len(dic)}。')
            return
        await session.send(s1)
        await session.send(f'赢家为：[CQ:at,qq={user_id}]，他的数字为：{num}, 获得积分{num*num}')
        zjjf(user_id, num*num)
        gg('con', 'id', 'min', 'con', 0)
        delete('mins')
        await news(dic, num)

@bot.on_message("private")
async def max(ctx:Context_T):
    massage = str(ctx['message'])
    user_id = str(ctx['user_id'])
    try:
        massage, num = massage.split(' ')
    except:
        massage, num = '', ''
    if massage == '#最大':
        if min() and num.isdigit():
            if day(user_id):
                await bot.send(ctx, '需要先签到的说~'+newgame, at_sender=True)
                return
            num = int(num)
            score = int(select('u', 'score', 'id', user_id)[0])
            if num>20 or num<=0:
                await bot.send(ctx, '只能在0——20中选哦~~')
                return
            if score < num:
                await bot.send(ctx, '积分不够哦~')
                return
            minnum(user_id, num)
            gg('u', 'id', user_id, 'score', score-num)
            await bot.send(ctx, f'参与成功，扣除积分{num}，请耐心等待结果。')



