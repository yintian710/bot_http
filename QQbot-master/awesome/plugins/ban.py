from jieba import posseg
from nonebot import(CommandSession, IntentCommand, NLPSession, on_command, on_natural_language,
    on_notice, NoticeSession, logger)
from nonebot.helpers import render_expression
from .tool import *

# 定义管理员请求时的「表达（Expression）」
EXPR_ADMIN = (
    '狗管理不要凑热闹',
    '我现在还不能禁言你呢'
)

EXPR_OWNER = (
    '你是群主，你开心就好。',
    '群主别闹了！',
    '没人能禁言你的！请不要@我！'
)


@on_command('ban', aliases=('#禁言', 'ban', '#关灯'), only_to_me=False)
async def ban(session: CommandSession):
    duration = int(session.get('duration', prompt='你想被禁言多少分钟呢？'))
    duration_sec = duration * 60
    user_id = session.ctx['sender']['user_id']
    name = session.ctx['sender']['nickname']
    # await bot.send_private_msg(user_id=1327960105, message=str(session.ctx['sender']))
    time = datetime.datetime.now().hour

    # 如果在群里发送，则在当前群禁言/解除
    if session.ctx['message_type'] == 'group':
        role = session.ctx['sender']['role']
        group_id = session.ctx['group_id']
        if group_id != 702052462 and user_id != 1327960105:
            return

        if role not in ['owners', 'admin']:
            await session.bot.set_group_ban(
                group_id=group_id, user_id=user_id, duration=duration_sec
            )

            if 0 <= time <= 6 and duration <= 480:
                score = int(duration / 10)
                try:
                    await bot.send_msg(group_id=group_id, message=f'{name}禁言成功，获得{score}积分')
                except:
                    await bot.send_msg(group_id=group_id, message=f'{int(user_id)} 禁言成功，获得{score}积分')
                zjjf(user_id, score)
        elif role == 'owner':
            await session.send(render_expression(EXPR_OWNER), at_sender=True)
        # elif role == 'admin':
        #     await session.send(
        #         render_expression(
        #             EXPR_ADMIN,
        #             user_id=user_id,
        #             duration=duration_sec,
        #         ),

                # at_sender=True
            # )

    # 如果私聊的话，则在所有小誓约支持的群禁言/解除
    # elif session.ctx['message_type'] == 'private':
    #     for group_id in session.bot.config.GROUP_ID:
    #         await session.bot.set_group_ban(
    #             group_id=group_id, user_id=user_id, duration=duration_sec
    #         )


@on_command('not_ban', aliases=('#解禁', '#开灯'), only_to_me=False)
async def not_ban(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    score = ye(user_id)
    if score > 50:
        kcjf(user_id, 50)
        await session.send('解除成功，扣除50积分。')
        await session.bot.set_group_ban(group_id=702052462, user_id=user_id, duration=0)


# @ban.args_parser
# async def _(session: CommandSession):
#     # 去掉消息首尾的空白符
#     stripped_arg = session.current_arg_text.strip()
#
#     if session.is_first_run:
#         # 该命令第一次运行（第一次进入命令会话）
#         if stripped_arg and stripped_arg.isdigit():
#             session.state['duration'] = int(stripped_arg)
#         return
#
#     if not stripped_arg:
#         session.pause('禁言时间不能为空呢，请重新输入')
#
#     # 检查输入参数是不是数字
#     if stripped_arg.isdigit():
#         session.state[session.current_key] = int(stripped_arg)
#     else:
#         session.pause('请只输入数字，不然我没法理解呢！')
#
#
# @on_natural_language(keywords={'#禁言'})
# async def _(session: NLPSession):
#     # 去掉消息首尾的空白符
#     stripped_msg = session.msg_text.strip()
#     # 对消息进行分词和词性标注
#     words = posseg.lcut(stripped_msg)
#
#     duration = None
#     # 遍历 posseg.lcut 返回的列表
#     for word in words:
#         # 每个元素是一个 pair 对象，包含 word 和 flag 两个属性，分别表示词和词性
#         if word.flag == 'm':
#             # m 表示数量
#             duration = word.word
#
#     # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
#     return IntentCommand(90.0, 'ban', current_arg=duration or '')


@on_notice
async def _(session: NoticeSession):
    logger.info('有新的通知事件：%s', session.event)
    print(session.event)


@on_notice('friend_add')
async def _(session: NoticeSession):
    await bot.set_friend_add_request(approve=True)
    await session.send('你好呀。')

@on_command('#special', aliases=('#头衔',), only_to_me=False)
async def _(session: CommandSession):
    user_id = session.ctx['sender']['user_id']
    group_id = session.ctx['group_id']
    score = ye(user_id)
    if score < 50:
        await session.send(pa, at_sender=True)
        return
    txt = session.get('txt', prompt='更改头衔需要花费50积分，请问请输入需要更改的头衔，输入0即退出。')
    if txt == '0':
        return
    for _ in ('银天', '銀天', '群主'):
        if _ in txt:
            await session.send(pa + ',扣你10积分，还皮不皮了？', at_sender=True)
            kcjf(user_id, 10)
            return
    if 0 < len(txt) <= 6:
        try:
            await bot.set_group_special_title(group_id=group_id, user_id=user_id, special_title=txt, self_id=2995739126)
            kcjf(user_id, 50)
            await session.send(f'花费50积分，设置头衔为{txt}成功。')
        except Exception as e:
            await session.send('失败了...')
    else:
        await session.send('长度要小于六个字的说...')