import commands.music.dismusic.errors as errors
import discord
from discord.ext import commands, tasks
import os
from os import path
import asyncio


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
async def on_command_error(ctx, error):
    name = 'No command'
    
    if isinstance(error, commands.CommandNotFound):
        return

    elif isinstance(error,commands.MemberNotFound):
        await log.logger(ctx,name,cog_name,'ERROR',error)
        await ctx.send(error)
        return

    elif isinstance(error,commands.MissingRequiredArgument):
        await log.logger(ctx,name,cog_name,'ERROR',error)
        await ctx.send("Invalid arguments. Please try again.")
        return

    elif isinstance(error,commands.CommandOnCooldown):
        return

    elif isinstance(error,commands.EmojiNotFound):
        return

    elif isinstance(error,errors.NotConnectedToVoice):
        await ctx.send(error)
        return

    elif isinstance(error,errors.PlayerNotConnected):
        await ctx.send(error)
        return

    elif isinstance(error,errors.MustBeSameChannel):
        await ctx.send(error)
        return

    else:
        await log.logger(ctx,name,cog_name,'ERROR',error)
        raise error
    
if __name__ == '__main__':

    omega= r"""   ____  __  __ ______ _____          
  / __ \|  \/  |  ____/ ____|   /\    
 | |  | | \  / | |__ | |  __   /  \   
 | |  | | |\/| |  __|| | |_ | / /\ \  
 | |__| | |  | | |___| |__| |/ ____ \ 
  \____/|_|  |_|______\_____/_/    \_\

"""
    print(omega)
    print("OMEGA BOT\nBy Xanthis\nVersion 1.019")
    print('----------')
    print('Loading Cogs')
    print('----------')
    client.lava_nodes = [
        {
            'host': 'lava.link',
            'port': 80,
            'rest_uri': 'http://lava.link:80',
            'identifier': 'MAIN',
            'password': 'OMEGA',
            'region': 'singapore'
        }
    ]
    load_cogs()
    print("All cogs loaded")
    print("----------")

    client.run(config.SECRET)
