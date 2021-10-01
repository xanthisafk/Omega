import codecs
from datetime import datetime

async def get_date():
    dt = datetime.now()
    date = '{:%B %d, %Y}'.format(dt)
    time = dt.strftime("%H:%M:%S")
    string = f'{date} {time}'
    return string

# Common logger. Logs in logs.txt
async def event_logger(ctx,name,cog):
    if name == 'aa':
        return
    try:
        date = await get_date()
        user = f'{ctx.author.name}#{ctx.author.discriminator}'
        string = f'{date} ({cog}): {user} used ({name})\n'
        f = codecs.open('./loggers/logs.txt', 'a', encoding='utf-8')
        f.write(string)
        f.close()

    except Exception as e:
        await error_logger(ctx,name,cog,e)

# Error logger. Logs in errors.txt
async def error_logger(ctx,name,cog,error):
    try:
        date = await get_date()
        user = f'{ctx.author.name}#{ctx.author.discriminator}'
        string = f'{date} ({cog}:"{name}"): {user} caused ({error})\n'
        f = codecs.open('./loggers/errors.txt', 'a', encoding='utf-8')
        f.write(string)
        f.close()

    except Exception as e:
        await admin_logger(ctx,name,cog,e)

# Admin logger. Logs in admin_errors.txt
async def admin_logger(ctx,name,cog,error=None,):
    try:
        date = await get_date()
        user = f'{ctx.author.name}#{ctx.author.discriminator}'
        if error == None:
            string = f'{date} ({cog}): {user} used ({name})\n'
        else:
            string = f'{date} ({cog}:"{name}"): {user} caused ({error})\n'

        f = codecs.open('./loggers/admin_errors.txt', 'a', encoding='utf-8')
        f.write(string)
        f.close()

    except Exception as e:
        # If all else fails, give up.
        raise e

async def db_logger(*,name,query=None):
    if name == 'aa':
        return
        
    date = await get_date()
    string = f'{date}: {name} ({query})\n'
    f = codecs.open('./loggers/queries.txt', 'a', encoding='utf-8')
    f.write(string)
    f.close()