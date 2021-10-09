import discord
from discord.ext import commands, tasks
import os
from os import path
import asyncio
import loggers.logger as log

import config

client = commands.Bot(command_prefix=config.PREFIX,case_insensitive=True)
client.remove_command('help')
cog_name = 'Main'

print('Hello Xanthis')

@tasks.loop(seconds=60)
async def change_presence():

        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over Nowhere Space"))
        await asyncio.sleep(60)
    
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=">help"))
        await asyncio.sleep(60)

        if path.exists('files/exists'):
            desc = 'on my PC!'
        else:
            desc = 'on Heroku!'
        
        await client.change_presence(activity=discord.Game(name=desc))
        await asyncio.sleep(60)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}.')
    print('Ready to go.')

    try:
        channel =  client.get_channel(config.DEBUG)

        if path.exists('./files/exists'):
            await channel.send(f"Logged in as {client.user.name}. Running on PC.")
        else:
            await channel.send(f"Logged in as {client.user.name}. Running on Heroku.")
    except: pass

    await change_presence.start()


@client.command()
async def load(ctx, extension = None):
    name = 'Load'
    if ctx.author.id in config.OWNER:
        if extension == None:
            for file in os.listdir('./cogs'):
                if file.endswith('.py') or file.startswith('!') == False:
                    try:
                        client.load_extension(f'cogs.{file[:-3]}')
                    except: pass
            print('loaded all')
        else:
            extension = extension.lower()
            client.load_extension(f'cogs.{extension}')
            print(f'{extension} loaded')
        await ctx.message.add_reaction('👍')
    await log.admin_logger(ctx,name,cog_name)


@load.error
async def load_error(ctx, error):
    name = 'Load'
    if isinstance(error, commands.CommandInvokeError):
        await ctx.message.add_reaction('👎')
        print(error)

    elif isinstance(error, commands.ExtensionNotLoaded):
        await ctx.message.add_reaction('👎')
        print(error)

    elif isinstance(error, commands.ExtensionAlreadyLoaded):
        await ctx.message.add_reaction('👎')
        print(error)

    else:
        raise error
    await log.admin_logger(ctx,name,cog_name,error)
    return

@client.command()
async def unload(ctx, extension = None):
    name = 'Unload'
    if ctx.author.id in config.OWNER:
        if extension == None:
            for file in os.listdir('./cogs'):
                if file.endswith('.py') or file.startswith('!') == False:
                    try:
                        client.unload_extension(f'cogs.{file[:-3]}')
                    except: pass
            print('unloaded all')
        else:
            extension = extension.lower()
            client.unload_extension(f'cogs.{extension}')
            print(f'{extension} unloaded')
        await ctx.message.add_reaction('👍')
    await log.admin_logger(ctx,name,cog_name)

@unload.error
async def unload_error(ctx, error):
    name = 'Unload'
    if isinstance(error, commands.CommandInvokeError):
        await ctx.message.add_reaction('👎')
        print(error)

    elif isinstance(error, commands.ExtensionNotLoaded):
        await ctx.message.add_reaction('👎')
        print(error)

    elif isinstance(error, commands.ExtensionAlreadyLoaded):
        await ctx.message.add_reaction('👎')
        print(error)
        
    else:
        raise error
    await log.admin_logger(ctx,name,cog_name,error)
    return


@client.command()
async def reload(ctx, extension = None):
    name = 'Reload'
    if ctx.author.id in config.OWNER:
        if extension == None:
            for file in os.listdir('./cogs'):
                if file.endswith('.py') or file.startswith('!') == False:
                    try:
                        client.unload_extension(f'cogs.{file[:-3]}')
                        client.load_extension(f'cogs.{file[:-3]}')
                    except: pass
            print('reloaded all')
        else:
            extension = extension.lower()
            client.unload_extension(f'cogs.{extension}')
            client.load_extension(f'cogs.{extension}')
            print(f'{extension} reloaded')
        await ctx.message.add_reaction('👍')
    await log.admin_logger(ctx,name,cog_name)

@reload.error
async def reload_error(ctx, error):
    name = 'Reload'
    if isinstance(error, commands.CommandInvokeError):
        await ctx.message.add_reaction('👎')
        print(error)

    elif isinstance(error, commands.ExtensionNotLoaded):
        await ctx.message.add_reaction('👎')
        print(error)

    elif isinstance(error, commands.ExtensionAlreadyLoaded):
        await ctx.message.add_reaction('👎')
        print(error)
        
    else:
        raise error
    await log.admin_logger(ctx,name,cog_name,error)
    return

for file in os.listdir('./cogs'):
    if file.endswith('.py') and file.startswith('!') == False:
        client.load_extension(f'cogs.{file[:-3]}')
        print(f'Loaded {file[:-3]}')

@client.event
async def on_command_error(ctx, error):
    name = 'No command'
    if isinstance(error, commands.CommandNotFound):
        await log.error_logger(ctx,name,cog_name,error)
        return
    
    elif isinstance(error,commands.MemberNotFound):
        await log.error_logger(ctx,name,cog_name,error)
        await ctx.send(error)
        return
    
    elif isinstance(error,commands.MissingRequiredArgument):
        await log.error_logger(ctx,name,cog_name,error)
        await ctx.send("Invalid arguments. Please try again.")
        print(error.args)
        return
    
    

    else:
        raise error

try:
    client.run(config.SECRET)
except Exception as e:
    if isinstance(e,RuntimeError):
        print("Exiting...")
    else:
        print("Unexpected exit.")
        raise e
