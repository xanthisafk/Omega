from datetime import datetime
import discord
from commands.music.music import InvalidRepeatMode
from discord.ext import commands, tasks
import os
from os import path
import traceback
from pyfiglet import figlet_format

import loggers.logger as log

import config

cog_name = 'Main'
client = commands.Bot(command_prefix=config.PREFIX,case_insensitive=True)
client.remove_command('help')


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}.')
    print('Ready to go.')
    print("----------")

    try:
        channel =  client.get_channel(config.DEBUG)

        if path.exists('./files/exists'):
            await channel.send(f"Logged in as {client.user.name}. Running on PC.")
            await log.debug(cog=cog_name,message='Running on PC')
        else:
            await channel.send(f"Logged in as {client.user.name}. Running on Heroku.")
            await log.debug(cog=cog_name,message='Running on Heroku')
    except: pass

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{config.PREFIX[0]}help"))


@client.command()
async def load(ctx, extension = None):
    """
    Loads the cog mentioned by user.

    args:
        extension: str -> name of extension.
    """
    name = 'Load'

    # Only works for owners of bot.
    if ctx.author.id in config.OWNER:

        # If no extension was provided
        if extension == None:

            # List folders in ./commands
            for dir in os.listdir('./commands'):

                # List files in ./commands/dir
                for file in os.listdir(f'commands/{dir}'):

                    # If file ends with .py and not starts with ! and is not atk.py
                    if file.endswith('.py') and not file.startswith('!'):
                        
                        #Attempts to load. If cog is already loaded, it will raise an exception which does nothing
                        try:
                            client.load_extension(f'commands.{dir}.{file[:-3]}')

                        except: pass

            print('>> Loaded: all')

        else:
            # Lower the extension text
            extension = extension.lower()

            # Get folders in /commands/
            for dir in os.listdir('./commands'):

                # Get files in /commands/dir
                for file in os.listdir(f'commands/{dir}'):

                    # If extension matches, load it
                    if extension == file[:-3]:
                        client.load_extension(f'commands.{dir}.{extension}')

            print(f'>> Loaded: {extension}')

        # Add success reaction
        await ctx.message.add_reaction(config.EMOTE_OK)
    await log.logger(ctx,name,cog_name,'INFO')
    return

@load.error
async def load_error(ctx, error):
    name = 'Load'
    await ctx.message.add_reaction(config.EMOTE_ERROR)
    await log.logger(ctx,name,cog_name,'ERROR',error)
    raise error

# ------------------------------------------------ #

@client.command()
async def unload(ctx, extension = None):
    """
    Unloads the cog mentioned by user.

    args:
        extension: str -> name of extension.
    """
    name = 'Unload'

    # Only works for owners of bot.
    if ctx.author.id in config.OWNER:

        # If no extension was provided
        if extension == None:

            # List folders in ./commands
            for dir in os.listdir('./commands'):

                # List files in ./commands/dir
                for file in os.listdir(f'commands/{dir}'):

                    # If file ends with .py and not starts with ! and is not atk.py
                    if file.endswith('.py') and not file.startswith('!') and not file == 'atk.py':
                        
                        #Attempts to unload. If cog is already unloaded, it will raise an exception which does nothing
                        try:
                            client.unload_extension(f'commands.{dir}.{file[:-3]}')

                        except: pass

            print('>> Unloaded: all')

        else:
            # Lower the extension text
            extension = extension.lower()

            # Get folders in /commands/
            for dir in os.listdir('./commands'):

                # Get files in /commands/dir
                for file in os.listdir(f'commands/{dir}'):

                    # If extension matches, unload it
                    if extension == file[:-3]:
                        client.unload_extension(f'commands.{dir}.{extension}')

            print(f'>> Unloaded: {extension}')

        # Add success reaction
        await ctx.message.add_reaction(config.EMOTE_OK)
    await log.logger(ctx,name,cog_name,'INFO')
    return

@unload.error
async def unload_error(ctx, error):
    name = 'Unload'
    await ctx.message.add_reaction(config.EMOTE_ERROR)
    await log.logger(ctx,name,cog_name,'ERROR',error)
    raise error

# ---------------------------------------------- #

@client.command()
async def reload(ctx, extension = None):
    """
    Reloads the cog mentioned by user.

    args:
        extension: str -> name of extension.
    """
    name = 'Reload'

    # Only works for owners of bot.
    if ctx.author.id in config.OWNER:

        # If no extension was provided
        if extension == None:

            # List folders in ./commands
            for dir in os.listdir('./commands'):

                # List files in ./commands/dir
                for file in os.listdir(f'commands/{dir}'):

                    # If file ends with .py and not starts with ! and is not atk.py
                    if file.endswith('.py') and not file.startswith('!') and not file == 'atk.py':
                        
                        #Attempts to reload. If cog is already unloaded, it will raise an exception which does nothing
                        try:
                            client.unload_extension(f'commands.{dir}.{file[:-3]}')
                            client.load_extension(f'commands.{dir}.{file[:-3]}')

                        except: pass

            print('>> Reloaded: all')

        else:
            # Lower the extension text
            extension = extension.lower()

            for dir in os.listdir('./commands'):
                for file in os.listdir(f'commands/{dir}'):
                    if extension == file[:-3]:
                        client.unload_extension(f'commands.{dir}.{extension}')
                        client.load_extension(f'commands.{dir}.{extension}')

            print(f'>> Reloaded: {extension}')

        # Add success reaction
        await ctx.message.add_reaction(config.EMOTE_OK)
    await log.logger(ctx,name,cog_name,'INFO')
    return

@reload.error
async def reload_error(ctx, error):
    name = 'Reload'
    await ctx.message.add_reaction(config.EMOTE_ERROR)
    await log.logger(ctx,name,cog_name,'ERROR',error)
    raise error

def load_cogs():
    for dir in os.listdir('./commands'):
        print(f'>> From {dir}')
        for file in os.listdir(f'commands/{dir}'):
            
                if file == 'logger.py':
                    try:
                        if config.DEBUG:
                            client.load_extension(f'commands{dir}.{file[:-3]}')
                            print()
                    except:
                        print("> Debug channel not set up. Logger not active.")
            
                elif file.endswith('.py') and file.startswith('!') == False and not file == 'logger.py':
                    client.load_extension(f'commands.{dir}.{file[:-3]}')
                    print(f'> Loaded: {file[:-3]}')

        print('----------')

@client.event
async def on_command_completion(ctx):

    try:
        cog = ctx.cog.qualified_name
    except:
        cog = 'None'

    await log.logger(ctx,ctx.command.name,cog,'INFO')
    try:
        channel =  client.get_channel(config.DEBUG)
        embed = discord.Embed(title='INFO', description=f'{ctx.author} used {ctx.invoked_with} in {ctx.channel.name}', color = discord.Color.blue(),timestamp=datetime.utcnow())
        await channel.send(embed=embed)
    except:
        pass

@client.event
async def on_command_error(ctx, error):
    try:
        cog = ctx.cog.qualified_name
    except:
        cog = 'None'
    if isinstance(error, commands.CommandInvokeError):
        await log.logger(ctx,ctx.command.name,cog,'ERROR',str(error.original))
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        await log.logger(ctx,ctx.command.name,cog,'ERROR',str(error))
    
    try:
        channel =  client.get_channel(config.DEBUG)
        embed = discord.Embed(title='ERROR', description=f'{ctx.author} used {ctx.command.name} in {ctx.channel.name}', color = discord.Color.red(),timestamp=datetime.utcnow())
        embed.add_field(name='Error', value=str(error))
        tb = traceback.format_exc()
        embed.add_field(name='Traceback',value=tb,inline=False)
        await channel.send(embed=embed)
    except:
        pass

    #raise error

    
if __name__ == '__main__':
    print(figlet_format(config.NAME,font='slant'))
    print("OMEGA BOT\nBy Xanthis\nVersion 1.2\nCreate an issue at https://github.com/xanthisafk/omega")
    print('----------')
    print('Loading Cogs')
    print('----------')
    load_cogs()
    print("All cogs loaded")
    print("----------")

    client.run(config.SECRET)
