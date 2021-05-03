from .bank import *

a = 0
b = 100
x = 0
play = ['id']
bool_m = 0
time3 = datetime.datetime.now()
time1 = time3
banker = ''
win = 0

def jl(a, b):
    if b-a == 100:
        return 66
    elif b-a >= 80:
        return 40
    elif b-a >= 30:
        return 24
    elif b-a >= 20:
        return 20
    elif b-a >= 10:
        return 14
    elif b-a > 3:
        return 10
    elif b-a == 3:
        return 8
    elif b-a == 2:
        return 6

@on_command('boom', aliases=('#数字炸弹', '#抓老鼠', '#洗小猪'), only_to_me=False)
async def boom(session: CommandSession):
    global x, a, b, bool_m, time1
    user_id = str(session.ctx['sender']['user_id'])
    if day(user_id):
        await session.send('需要先签到的说~'+newgame, at_sender=True)
        return
    time2 = datetime.datetime.now()
    t = (time2-time1).seconds
    lq = 1
    if bool_m:
        await session.send(f'游戏开了都不知道？丢脸！\n目前可查找猪圈范围：{a}-{b}', at_sender=True)
        return
    if t < lq:
        if user_id == '1327960105':
            await session.send(f'爸爸再等一下哦~还有{lq-t}秒~', at_sender=True)
        else:
            await session.send(f'还差{lq-t}秒才能开，耐心就这？就这？', at_sender=True)
        return
    time1 = time2
    res = select('game', 'boom', 'id', user_id)
    if not res:
        cur.execute(f'insert into game(id, boom) value ({user_id}, 1)')
        x = random.randint(1, 99)
        a = 0
        b = 100
        bool_m = 1
        await session.send(f'启动成功,🐷躲在第1-100间猪圈中，请输入{a}到{b}中间的数字找到它，就可以把它洗干净啦！越早找到奖励越多。')
    elif res[0] == 1:
        if user_id == '1327960105':
            await session.send('爸爸你开过了，明天再来哦~', at_sender=True)
        else:
            await session.send('开过一次还不满足？爬！', at_sender=True)
        time1 = time3
    elif res[0] == 0:
        gg('game', 'id', user_id, 'boom', 1)
        x = random.randint(1, 99)
        a = 0
        b = 100
        bool_m = 1
        await session.send(f'启动成功,🐷躲在第1-100间猪圈中，请输入{a}到{b}中间的数字找到它，就可以把它洗干净啦！越早找到奖励越多。')
    con.commit()

@on_command('numboom', aliases='num', permission=permission.SUPERUSER)
async def zboom(session: CommandSession):
    global x, a, b, bool_m, time1
    time1 = datetime.datetime.now()
    x = random.randint(1, 99)
    a = 0
    b = 100
    bool_m = 1
    await session.send(f'启动成功,🐷躲在第1-100间猪圈中，请输入{a}到{b}中间的数字找到它，就可以把它洗干净啦！越早找到奖励越多。')


@on_command('z_boom', aliases=('#庄家抓老鼠', '#庄家洗小猪'), only_to_me=False)
async def boom(session: CommandSession):
    global x, a, b, bool_m, time1, banker
    user_id = str(session.ctx['sender']['user_id'])
    if day(user_id):
        await session.send('需要先签到的说~'+newgame, at_sender=True)
        return
    time2 = datetime.datetime.now()
    t = (time2-time1).seconds
    lq = 1
    if bool_m:
        if user_id == banker:
            await session.send(f'比赛开启成功，目前可查找猪圈范围：{a}-{b}')
        else:
            await session.send(f'游戏开了都不知道？丢脸！\n目前可查找猪圈范围：{a}-{b}', at_sender=True)
        return
    if not session.ctx.group_id:
        x = int(session.get('x', prompt='请输入游戏的答案'))
        if x >= 100 or x <= 0:
            await session.send('给爷爬！游戏范围都不知道了？')
            return
    if t < lq:
        if user_id == '1327960105':
            await session.send(f'爸爸再等一下哦~还有{lq-t}秒~', at_sender=True)
        else:
            await session.send(f'还差{lq-t}秒才能开，耐心就这？就这？', at_sender=True)
        return
    score = ye(user_id)
    if score < 70:
        yes = session.get('yes', prompt='您的积分不够开启一场比赛，是否通过银行借70积分？回答1为借，0或其他不借。')
        if yes == '1':
            a, b = loan_t(user_id)
            if a != 0:
                await session.send('你还有未还借款，无法再借。')
                return
            elif a == '查无此人':
                await session.send('请先在银行开户哦~')
                return
            bank(user_id, 70)
        else:
            return
    score = ye(user_id)
    gg('u', 'id', user_id, 'score', score-70)
    time1 = time2
    banker = user_id
    if session.ctx.group_id:
        x = random.randint(1, 99)
    a = 0
    b = 100
    bool_m = 2
    await session.send(f'启动成功,🐷躲在第1-100间猪圈中，请输入{a}到{b}中间的数字找到它，就可以把它洗干净啦！越早找到奖励越多。')


@on_command('mm', aliases='mm', permission=permission.SUPERUSER)
async def zboom(session: CommandSession):
    global x
    await bot.send_msg(user_id=1327960105, message=str(x))
    await session.send(' ')


@bot.on_message('group')
async def group_msg(ctx: Context_T):
    global x, a, b, play, bool_m, win, banker
    s = str(ctx['message'])
    user_id = str(ctx['user_id'])
    if s.isdigit():
        if bool_m == 1:
            if day(user_id):
                await bot.send(ctx, '需要先签到的说~'+newgame, at_sender=True)
                return
            if user_id == play[-1]:
                await bot.send(ctx, '说了多少遍不能连续玩两次?!给爷爬!', at_sender=True)
                return
            score = int(select('u', 'score', 'id', user_id)[0])
            if score < 1:
                await bot.send(ctx, '没积分玩尼玛呢！', at_sender=True)
                return
            play.append(user_id)
            if a < int(s) < b:
                n = int(s)
                if n == x:
                    j = jl(a, b)
                    await bot.send(ctx, f'你找到了🐷！并把它洗了个干净！此外获得{j}积分。', at_sender=True)
                    gg('u', 'id', user_id, 'score', score + j)
                    a = 0
                    b = 100
                    play = ['id']
                    bool_m = 0
                elif n < x:
                    a = n
                    await bot.send(ctx, f'找错了猪圈，扣除1积分，接下来输入{a}到{b}之间的猪圈数,求你了快点找到!', at_sender=True)
                    gg('u', 'id', user_id, 'score', score - 1)
                elif n > x:
                    b = n
                    await bot.send(ctx, f'找错了猪圈，扣除1积分，接下来输入{a}到{b}之间的猪圈数,求你了快点找到!', at_sender=True)
                    gg('u', 'id', user_id, 'score', score - 1)
            else:
                await bot.send(ctx, f'找错了猪圈，扣除1积分，接下来输入{a}到{b}之间的猪圈数,求你了快点找到!', at_sender=True)
                gg('u', 'id', user_id, 'score', score - 1)
        elif bool_m == 2:
            if day(user_id):
                await bot.send(ctx, '需要先签到的说~'+newgame, at_sender=True)
                return
            if user_id == play[-1]:
                await bot.send(ctx, '说了多少遍不能连续玩两次?!给爷爬!', at_sender=True)
                return
            if user_id == banker:
                await bot.send(ctx, '自己开的不能自己玩！给爷爬！')
                return
            score = int(select('u', 'score', 'id', user_id)[0])
            if score < 1:
                await bot.send(ctx, '没积分玩尼玛呢！', at_sender=True)
                return
            play.append(user_id)
            if a < int(s) < b:
                n = int(s)
                if n == x:
                    j = jl(a, b)/2
                    await bot.send(ctx, f'你找到了🐷！并把它洗了个干净！此外获得{j}积分。', at_sender=True)
                    gg('u', 'id', user_id, 'score', score + j)
                    wins = 70+win-j-4
                    score1 = int(select('u', 'score', 'id', banker)[0])
                    gg('u', 'id', banker, 'score', score1 + wins)
                    win = 0
                    a = 0
                    b = 100
                    play = ['id']
                    bool_m = 0
                    await bot.send_msg(user_id=banker, message=f'您做庄的数游戏已结束,扣除4积分启动分，玩家获胜分{j}\n'
                                                               f'玩家总参与积分{win}\n返还给您{wins}积分。')
                elif n < x:
                    a = n
                    await bot.send(ctx, f'找错了猪圈，扣除1积分，接下来输入{a}到{b}之间的猪圈数,求你了快点找到!', at_sender=True)
                    gg('u', 'id', user_id, 'score', score - 1)
                    win += 1
                elif n > x:
                    b = n
                    await bot.send(ctx, f'找错了猪圈，扣除1积分，接下来输入{a}到{b}之间的猪圈数,求你了快点找到!', at_sender=True)
                    gg('u', 'id', user_id, 'score', score - 1)
                    win += 1
            else:
                await bot.send(ctx, f'找错了猪圈，扣除1积分，接下来输入{a}到{b}之间的猪圈数,求你了快点找到!', at_sender=True)
                gg('u', 'id', user_id, 'score', score - 1)
                win += 1
