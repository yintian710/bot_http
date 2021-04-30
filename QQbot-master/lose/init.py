from lose.cg import *
from awesome.plugins.clock import *


@on_command('who', aliases=('#名字', '#姓名', '#叫什么'), only_to_me=False)
async def who(session: CommandSession):
    await session.send('My name is "cp"', at_sender=True)


@on_command('sex', aliases=('#性别', "#男还是女"), only_to_me=False)
async def sex(session: CommandSession):
    await session.send('secret', at_sender=True)


@on_command('gmgp', aliases=('#购买原始股票', '原始股票购买', 'gmgp',), only_to_me=False)
async def gmgp(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    if time():
        if day(user_id):
            await session.send('需要先签到的说~'+newgame, at_sender=True)
            return
        str1 = await scgp()
        gm = session.get('gm', prompt=str1, at_sender=True)
        gm, num1 = gm.split(' ')
        if gm not in gp:
            await session.send('股票代码错误', at_sender=True)
        else:
            ret = await buy(user_id, gm, num1)
            await session.send(ret, at_sender=True)
    else:
        await session.send('亲`股市还未开盘哦~！推荐新游戏：猜猜谁最大。')


# @on_command('csgp', aliases=('#出售股票', 'cs'), only_to_me=False)
# async def csgp(session: CommandSession):
#     user_id = str(session.ctx['sender']['user_id'])
#     str1 =await scgp()
#     sc = session.get('csgp', prompt='你想出售哪只股票？\n'+str1, at_sender=True)
#     num = session.get('num', prompt='想要出售多少?', at_sender=True)
#     ret = await sell(user_id, sc, num)
#     await session.send(ret, at_sender=True)

@on_command('gpjy', aliases=('#市场购买', '#购买股票', '#股票购买', 'scgm'), only_to_me=False)
async def scgm(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    if time():
        if day(user_id):
            await session.send('需要先签到的说~'+newgame, at_sender=True)
            return
        gpdm = session.get('gpdm', prompt='请输入“股票代码 购买数量 理想购买价格”\n', at_sender=True)
        gpdm, num1, jg = gpdm.split(' ')
        if gpdm not in gp:
            await session.send('股票代码错误', at_sender=True)
        else:
            ret = await gpjy(user_id, gpdm, num1, jg)
            await session.send(ret, at_sender=True)
    else:
        await session.send('亲`股市未开盘哦~！推荐新游戏：猜猜谁最大。')


@on_command('gpgd', aliases=('#市场挂单', '#市场出售', '#股票出售', '#出售股票', 'scgd'), only_to_me=False)
async def scgd(session: CommandSession):
    if time():
        user_id = str(session.ctx['sender']['user_id'])
        if day(user_id):
            await session.send('需要先签到的说~'+newgame, at_sender=True)
            return
        gpdm = session.get('gpdm', prompt='请输入“出售股票代码 出售数量 理想出售单价”？\n', at_sender=True)
        gpdm, num1, jg = gpdm.split(' ')
        if gpdm not in gp:
            await session.send('股票代码错误', at_sender=True)
        else:
            ret = await gpgd(user_id, gpdm, num1, jg)
            await session.send(ret, at_sender=True)
    else:
        await session.send('亲`股市还未开盘哦~,推荐新游戏：猜猜谁最大。')


@on_command('jysc', aliases=('#交易市场', '#市场查询', '查询市场', 'jy'), only_to_me=False)
async def cxgp(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    sc = session.get('sc', prompt='"请输入想查询的股票代码，1表示查询自己的订单”？\n', at_sender=True)
    str1 = await sec1(sc, user_id)
    await session.send(str1, at_sender=True)


@on_command('ql', aliases=('#订单撤销', '清理订单', '#撤销订单', 'cx'), only_to_me=False)
async def cxdd(session: CommandSession):
    user_id = str(session.ctx['sender']['user_id'])
    dh = session.get('dh', prompt='请输入“需要撤销的订单号”\n', at_sender=True)
    cx = await clean(dh, user_id)
    await session.send(cx, at_sender=True)



    # await session.send('功能暂时下架', at_sender=True)






