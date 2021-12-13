from datetime import datetime
import discord
from discord.ext import commands
import os
from os import path
import traceback
from pyfiglet import figlet_format
from random import choice
import subprocess
import sys
import requests

import loggers.logger as log

import json
import codecs

with codecs.open('config.json', 'r', encoding='utf-8') as f:
            r = json.load(f)
            PREFIX = r['general']['PREFIX']
            TOKEN = r['general']['TOKEN']

cog_name = 'Main'
intents = discord.Intents.all()
client = commands.Bot(command_prefix=PREFIX,case_insensitive=True, intents=intents)
client.remove_command('help')
client.config = r


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}.')
    print('Ready to go.')
    print("----------")

    try:
        channel =  client.get_channel(client.config['debug']['CHANNEL'])

        if path.exists('./files/exists'):
            await channel.send(f"Logged in as {client.user.name}. Running on PC.")
            await log.debug(cog=cog_name,message='Running on PC')
        else:
            await channel.send(f"Logged in as {client.user.name}. Running on Heroku.")
            await log.debug(cog=cog_name,message='Running on Heroku')
    except: pass

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{PREFIX[0]}help"))


@client.command()
async def load(ctx, extension = None):
    """
    Loads the cog mentioned by user.

    args:
        extension: str -> name of extension.
    """

    # Only works for owners of bot.
    if ctx.author.id in client.config['general']['OWNER']:

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
                        except:
                            pass

            await ctx.send(f'>> Loaded: all')

            print('>> Loaded: all')

        else:
            # Lower the extension text
            extension = extension.lower()

            # Get folders in /commands/
            broken = False
            for dir in os.listdir('./commands'):

                # Get files in /commands/dir
                for file in os.listdir(f'./commands/{dir}'):

                    # If extension matches, load it
                    if extension == file[:-3]:
                        print(extension, file)
                        client.load_extension(f'commands.{dir}.{extension}')

                        print(f'>> Loaded: {extension}')
                        broken = True
                        break
                
                if broken:
                    break

            else:
                await ctx.message.add_reaction(client.config['emotes']['ERROR'])
                return print(f'>> Could not find {extension}')


        # Add success reaction
        await ctx.message.add_reaction(client.config['emotes']['OK'])
    return

@load.error
async def load_error(ctx, error):
    name = 'Load'
    await ctx.message.add_reaction(client.config['emotes']['ERROR'])
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
    if ctx.author.id in client.config['general']['OWNER']:

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
        await ctx.message.add_reaction(client.config['emotes']['OK'])
    await log.logger(ctx,name,cog_name,'INFO')
    return

@unload.error
async def unload_error(ctx, error):
    name = 'Unload'
    await ctx.message.add_reaction(client.config['emotes']['ERROR'])
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
    if ctx.author.id in client.config['general']['OWNER']:

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
        await ctx.message.add_reaction(client.config['emotes']['OK'])
    await log.logger(ctx,name,cog_name,'INFO')
    return

@reload.error
async def reload_error(ctx, error):
    name = 'Reload'
    await ctx.message.add_reaction(client.config['emotes']['ERROR'])
    await log.logger(ctx,name,cog_name,'ERROR',error)
    raise error

def load_cogs():
    for dir in os.listdir('./commands'):
        print(f'>> From {dir}')
        for file in os.listdir(f'commands/{dir}'):
            
                if file == 'logger.py':
                    try:
                        if client.config["debug"]["CHANNEL"]:
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
        channel =  client.get_channel(client.config['debug']['CHANNEL'])
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
        channel =  client.get_channel(client.config['debug']['CHANNEL'])
        embed = discord.Embed(title='ERROR', description=f'{ctx.author} used {ctx.command.name} in {ctx.channel.name}', color = discord.Color.red(),timestamp=datetime.utcnow())
        embed.add_field(name='Error', value=str(error))
        tb = traceback.format_exc()
        embed.add_field(name='Traceback',value=tb,inline=False)
        await channel.send(embed=embed)
    except:
        pass

    


def download_lavalink(url: str, dest_folder='lib'):
    print("Lavalink is not installed.\nDownloading Lavalink...")
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    filename = "Lavalink.jar"
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("Saving Lavalink to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


def setup_dependencies():
    # install requirements via pip
    print("Installing Dependencies...")
    subprocess.check_call([sys. executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
    # check if Lavalink.jar exists
    if not os.path.exists('lib/Lavalink.jar'):
        lavalink_url = "https://github.com/freyacodes/Lavalink/releases/download/3.4/Lavalink.jar"
        download_lavalink(lavalink_url)

    print("Dependencies installed.\nStarting Lavalink")
    
    subprocess.Popen(['java', '-jar', 'lib/Lavalink.jar'])

    
if __name__ == '__main__':
    setup_dependencies()
    font = choice(['graffiti', 'ogre', 'rectangles', 'roman', 'slant', 'standard'])
    print(figlet_format(client.config['general']['NAME'],font=font))
    print("OMEGA BOT\nBy Xanthis\nVersion 1.2\nCreate an issue at https://github.com/xanthisafk/omega")
    print('----------')
    print('Loading Cogs')
    print('----------')
    load_cogs()
    print("All cogs loaded")
    print("----------")

    client.run(TOKEN)
