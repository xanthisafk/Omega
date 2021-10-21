import codecs
from datetime import datetime

async def get_date():
    dt = datetime.now()
    return dt.strftime("%B %d, %Y %H:%M:%S")

async def write(string):
    f = codecs.open('./loggers/logs.txt', 'a', encoding='utf-8')
    f.write(string)
    f.close()

async def logger(ctx,name,cog,level,message=None):
    if name == 'aa':
        return
    
    date = await get_date()
    user = f'{ctx.author.name}#{ctx.author.discriminator}'

    string = f'[{level}]{date} ({cog}): {user} used ({name})'

    if message != None:
        string += f': {message}\n'
    else:
        string+='\n'

    await write(string)

async def debug(**kwargs):
    date = await get_date()
    await write(f'{date}: {kwargs}\n')

async def db_logger(*,name,query=None):
    if name == 'aa':
        return

    date = await get_date()
    string = f'{date}: {name} ({query})\n'
    f = codecs.open('./loggers/queries.txt', 'a', encoding='utf-8')
    f.write(string)
    f.close()
