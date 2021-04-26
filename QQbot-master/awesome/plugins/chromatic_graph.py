from .tool import *


@on_command('chromatic_graph', aliases=('#色图', '#涩图'), only_to_me=False)
async def _(session: CommandSession):
    num = random.randint(1, 6)
    str1 = f'[CQ:image,file=file:///C:\\Users\\Administrator\\Desktop\\bot\\data\\images\image\\{num}.jpg]'
    str1 += '啧啧啧！[CQ:face,id=178]'
    await session.send(str1)
