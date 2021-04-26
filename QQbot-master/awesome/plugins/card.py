from aiocqhttp import MessageSegment
from .tool import *


# def cd(user_id, img, lv, num=1):  # 存档
#     img = img[:-4]
#     cur.execute(f'update card set {img}={img}+1 where id={user_id}')
#     con.commit()
#     cur.execute(f'update u set {lv}={lv}+1 where id={user_id}')
#     con.commit()

def cd(user_id, img, lv, num=1):  # 存档
    if '.jpg' in img:
        img = img[:-4]
    print(img)
    cur.execute(f'select {img} from card where id = {user_id}')
    # img_num = select('card', img, 'id', user_id)[0]
    img_num = cur.fetchone()[0]
    lv_num = select('u', lv, 'id', user_id)[0]
    cur.execute(f'update card set {img}={img_num + num} where id={user_id}')
    con.commit()
    cur.execute(f'update u set {lv}={lv_num + num} where id={user_id}')
    con.commit()


def card_list(user_id):
    list1 = []
    for i in card_img:
        str1 = f'{i}:\n'
        for _ in card_img[i]:
            cur.execute(f'select {_[:-4]} from card where id = {user_id}')
            res = cur.fetchone()
            str1 += f'{_[:-4]}:{res[0]}\n'
        list1.append(str1)
    return list1


def mycard(user_id):
    cur.execute(f'select N, R, SR, SSR, UR from u where id = {user_id}')
    res = cur.fetchone()
    str1 = f'N:{res[0]}  R:{res[1]}  SR:{res[2]}  SSR:{res[3]}  UR:{res[4]}'
    return str1


def random_img():
    UR = UR_num
    SSR = UR + SSR_num * 3
    SR = SSR + SR_num * 9
    R = SR + R_num * 27
    N = R + N_num * 81
    a = random.randint(0, N)
    if a < UR:
        img = UR_img[random.randint(0, len(UR_img) - 1)]
        str1 = '获得UR!!!欧皇再世！——' + img[:-4]
        lv = 'UR'
    elif a < SSR:
        img = SSR_img[random.randint(0, len(SSR_img) - 1)]
        str1 = '获得SSR!!!——' + img[:-4]
        lv = 'SSR'
    elif a < SR:
        img = SR_img[random.randint(0, len(SR_img) - 1)]
        str1 = '获得SR!——' + img[:-4]
        lv = 'SR'
    elif a < R:
        img = R_img[random.randint(0, len(R_img) - 1)]
        str1 = '获得R!——' + img[:-4]
        lv = 'R'
    else:
        img = N_img[random.randint(0, len(N_img) - 1)]
        str1 = '获得N!——' + img[:-4]
        lv = 'N'
    return img, str1, lv


async def cardsell(user_id, txt):
    x = txt.split(' ')
    id = nums(x[0])
    lv = level[x[1]]
    cur.execute(f'select {x[1]} from card where id = %s', user_id)
    res = cur.fetchone()[0]
    if res < 1:
        return '爬！', 0
    if id == user_id:
        return '左手转右手小心扣了你的！', 0
    cd(user_id, x[1], lv, -1)
    cd(id, x[1], lv, 1)
    return f'交易成功,{x[1]}已送出。', 1


def achieve_one(achieve, user_id):
    cur.execute(f'select * from card where id = {user_id}')
    res = cur.fetchone()
    card = {}
    for i in range(1, len(res)):
        card[cardlist[i]] = res[i]
    nice = 1
    str1 = f'您的成就 {achieve} 缺少如下卡片:'
    for i in achieve_list[achieve]:
        if card[i] == 0:
            nice = 0
            str1 += i + ' '
    if nice == 1:
        return f'{achieve} ', ''
    else:
        return '', str1 + '\n'


def new_achieve(img, user_id):
    ach = '获得新成就：'
    cur.execute(f'select achievement from u where id = {user_id}')
    res = cur.fetchone()[0]
    if res:
        achs = res.split(' ')
    else:
        achs = ''
    bool = False
    for i in achieve_list:
        if img in achieve_list[i] and i not in achs:
            str1, str2 = achieve_one(i, user_id)
            if str1:
                ach += str1
                res += str1
                cur.execute(f'update u set achievement = "{res}" where id = {user_id}')
                bool = True
    return ach, bool


@on_command('ck', aliases=('#抽卡', '#单抽出奇迹', '#单抽出奇迹！'), only_to_me=False)
async def card(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    if day(user_id):
        await session.send('需要先签到的说~' + newgame, at_sender=True)
        return
    cur.execute(f'select * from card where id = {user_id}')
    res = cur.fetchone()
    if not res:
        await session.send('需要先注册哦：#注册')
        return
    score = ye(user_id)
    if score < card_price:
        await session.send(pa, at_sender=True)
        return
    kcjf(user_id, card_price)
    img, str1, lv = random_img()
    img = img[:-4]
    # if user_id == '1327960105':
    #     img = '团子'
    #     lv = 'SR'
    str1 = f'花费{card_price}积分，获得{lv}卡：{img}。'
    await session.send(str1, at_sender=True)
    # await session.send(f'[CQ:lose, file=ck\\{img}]')
    cd(user_id, img, lv, 1)
    print(img)
    ach, bool = new_achieve(img, user_id)
    if bool:
        await session.send(ach)


@on_command('sl', aliases=('#十连改命！', '#十连', '#传统手艺',), only_to_me=False)
async def ten_card(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    if day(user_id):
        await session.send('需要先签到的说~' + newgame, at_sender=True)
        return
    cur.execute(f'select * from card where id = {user_id}')
    res = cur.fetchone()
    if not res:
        await session.send('需要先注册哦：#注册', at_sender=True)
        return
    score = ye(user_id)
    if score < card_price * 9:
        await session.send(pa, at_sender=True)
        return
    kcjf(user_id, card_price * 9)
    imgs = []
    l1 = f'花费{card_price * 9}积分。\n'
    str2 = ''
    n_NUM = 0
    for i in range(10):
        img, str1, lv = random_img()
        n_NUM += 1 if lv == 'N' else 0
        if n_NUM == 10:
            while lv == 'N':
                img, str1, lv = random_img()
                l1 += '触发保底：\n'
        imgs.append(img)
        cd(user_id, img, lv, 1)
        if str1:
            l1 += str1 + '\n'
    for _ in imgs:
        str2 += f'[CQ:image, file=ck\\{_}]'
        _ = _[:-4]
        ach, bool = new_achieve(_, user_id)
        if bool:
            await session.send(ach)
    if user_id != '942788328':
        zjjf(942788328, 5)
    await session.send(l1, at_sender=True)
    # await session.send(str2)


@on_command('ssl', aliases=('#百连', '#有钱任性', '#终极奥义'), only_to_me=False)
async def ten_card(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    if day(user_id):
        await session.send('需要先签到的说~' + newgame, at_sender=True)
        return
    cur.execute(f'select * from card where id = {user_id}')
    res = cur.fetchone()
    if not res:
        await session.send('需要先注册哦：#注册', at_sender=True)
        return
    score = ye(user_id)
    if score < card_price * 80:
        await session.send(pa, at_sender=True)
        return
    kcjf(user_id, card_price * 80)
    imgs = []
    str2 = ''
    lv_num = {'UR': 0, "SSR": 0, 'SR': 0, 'R': 0, 'N': 0}
    card_num = {'N': [], 'R': [], 'SR': [], "SSR": [], 'UR': []}
    for i in range(10):
        for i in range(10):
            img, str1, lv = random_img()
            lv_num[lv] += 1
            imgs.append(img)
            cd(user_id, img, lv, 1)
            card_num[lv].append(img)
    for _ in imgs:
        str2 += f'[CQ:image, file=ck\\{_}]'
        _ = _[:-4]
        ach, bool = new_achieve(_, user_id)
        if bool:
            await session.send(ach)
    if user_id != '942788328':
        zjjf(942788328, 50)
    await session.send(f'扣除{card_price * 80}积分\n'
                       f'获得UR卡{lv_num["UR"]}张\n'
                       f'获得SSR卡{lv_num["SSR"]}张\n'
                       f'获得SR卡{lv_num["SR"]}张\n'
                       f'获得R卡{lv_num["R"]}张\n'
                       f'获得N卡{lv_num["N"]}张\n'
                       f'详细抽卡结果已私聊发送', at_sender=True)
    str3 = ''
    for i in card_num:
        if i == 'N':
            str3 += '获得N卡若干\n'
            continue
        if not card_num[i]:
            continue
        for _ in card_num[i]:
            str3 += f'获得{i}——{_}\n'
    await bot.send_private_msg(user_id=user_id, message=str3)


def zc(id):
    cur.execute(f'select * from card where id={id}')
    res = cur.fetchone()
    if res:
        return '你已经注册过了'
    cur.execute(f'insert into card(id) value({id}) ')
    con.commit()
    return '注册成功'


@on_command('zhuce', aliases='#注册', only_to_me=False)
async def vhuce(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    if day(user_id):
        await session.send('需要先签到的说~' + newgame, at_sender=True)
        return
    str1 = zc(user_id)
    await session.send(str1, at_sender=True)


@on_command('my_card', aliases='#我的卡牌', only_to_me=False)
async def my_card(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    bot = nonebot.get_bot()
    str1 = mycard(user_id)
    list1 = card_list(user_id)
    await session.send(str1, at_sender=True)
    for _ in list1:
        await bot.send_msg(user_id=user_id, message=_)


@on_command('card_sell', aliases=('#卡牌交易', '#交易卡牌'), only_to_me=False)
async def card_sell(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    name = session.ctx['sender']['nickname']
    if day(user_id):
        await session.send('需要先签到的说~' + newgame, at_sender=True)
        return
    txt = session.get('txtn', prompt='请输入@要交易的人+卡牌名字\n')
    t1, bool = await cardsell(user_id, txt)
    await session.send(t1, at_sender=True)
    if bool:
        x = txt.split(' ')
        id = nums(x[0])
        ach, bool1 = new_achieve(x[1], id)
        if bool1:
            x = txt.split(' ')
            id = nums(x[0])
            await session.send(f'{name}的交易对象' + ach)


@bot.on_message()
async def _(ctx: Context_T):
    massage = str(ctx['message'])
    user_id = str(ctx['user_id'])
    try:
        massage, name = massage.split(' ')
    except:
        name = ''
    if massage == '#卡牌':
        cur.execute(f'select {name} from card where id = "{user_id}"')
        res = cur.fetchone()[0]
        if res != 0:
            await bot.send_msg(group_id=ctx['group_id'],
                               message=f'[CQ:image,file=file:///C:\\Users\\Administrator\\Desktop\\bot\\data\\images\ck\\card\\{
                               level[name]}\\{name}.jpg]')
        else:
            await bot.send_msg(group_id=ctx['group_id'],
                               message=pa)


@on_command('sell_card_N', aliases='#出售N卡', only_to_me=False)
async def sell_card_N(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    cur.execute(f'select * from card where id = {user_id}')
    res = cur.fetchone()[1:]
    list = cardlist[1:]
    sum = 0
    for num, _ in enumerate(list):
        if _ + '.jpg' in N_img and res[num] > 1:
            sum += res[num] - 1
            gg('card', 'id', user_id, _, 1)
    zjjf(user_id, sum)
    cur.execute(f'update u set N = N-{sum} where id = {user_id}')
    con.commit()
    if sum == 0:
        return
    await session.send(f'共出售{sum}张N卡，获得积分{sum}。')


@on_command('sell_card_R', aliases='#出售R卡', only_to_me=False)
async def sell_card_R(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    cur.execute(f'select * from card where id = {user_id}')
    res = cur.fetchone()[1:]
    list = cardlist[1:]
    sum = 0
    for num, _ in enumerate(list):
        if _ + '.jpg' in R_img and res[num] > 1:
            sum += res[num] - 1
            gg('card', 'id', user_id, _, 1)
    zjjf(user_id, sum * 3)
    cur.execute(f'update u set R = R-{sum} where id = {user_id}')
    con.commit()
    if sum == 0:
        return
    await session.send(f'共出售{sum}张R卡，获得积分{sum * 3}。')


@on_command('sell_card_SR', aliases='#出售SR卡', only_to_me=False)
async def sell_card_SR(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    cur.execute(f'select * from card where id = {user_id}')
    res = cur.fetchone()[1:]
    list = cardlist[1:]
    sum = 0
    for num, _ in enumerate(list):
        if _ + '.jpg' in SR_img and res[num] > 1:
            sum += res[num] - 1
            gg('card', 'id', user_id, _, 1)
    zjjf(user_id, sum * 7)
    cur.execute(f'update u set SR = SR-{sum} where id = {user_id}')
    con.commit()
    if sum == 0:
        return
    await session.send(f'共出售{sum}张R卡，获得积分{sum * 7}。')


@on_command('achievement', aliases='#我的成就', only_to_me=False)
async def my_achieve(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    cur.execute(f'select achievement from u where id = {user_id}')
    res = cur.fetchone()[0]
    num = len(res.split(' ')) - 1
    str1 = f'您的成就有：{res}， 共{num}个'
    await session.send(str1)


@on_command('select_achievement', aliases='#成就进度', only_to_me=False)
async def select_achieve(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    str1 = ''
    for _ in achieve_list:
        str3, str2 = achieve_one(_, user_id)
        str1 += str2
    await bot.send_msg(user_id=user_id, message=str1)


@on_command('ccc', aliases='#卡', only_to_me=False)
async def select_achieve(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    try:
        await session.send('1')
        #     await session.send('[CQ:image, file=s1.image]')
        # except:
        #     await session.send('s1')
        # try:
        await session.send(r'[CQ:image,file=file:///C:\Users\Administrator\Desktop\bot\data\images\qq.jpg]')
    except:
        await session.send(f'image')


@bot.on_message()
async def achieve(ctx: Context_T):
    message = str(ctx['message'])
    user_id = str(ctx['user_id'])
    try:
        message = message.split(' ')
    except:
        pass
    if message[0] == '#卡牌出售':
        card1 = ''
        try:
            for i in range(1, len(message)):
                cur.execute(f'select {message[i]} from card where id = {user_id}')
                res = cur.fetchone()[0]
                if res != 0:
                    lv = level[message[1]]
                    cur.execute(f'update card set {message[i]}={message[i]}-1 where id={user_id}')
                    con.commit()
                    cur.execute(f'update u set {lv}={lv}-1,score=score+{re_price[lv]} where id={user_id}')
                    con.commit()
                    card1 += message[i] + ' '
            await bot.send_msg(group_id=ctx['group_id'], message='出售成功')
        except:
            await bot.send_msg(group_id=ctx['group_id'], message=card1 + '出售成功')
