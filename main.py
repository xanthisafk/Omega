import discord
from discord.ext import commands
import config
import os
from os import path

intents = discord.Intents(messages=True,members=True,emojis=True,guilds=True)
client = commands.Bot(command_prefix = config.PREFIX, case_insensitive = True, intents = intents)
client.remove_command('help')

@client.event
async def on_ready():
    

    channel =  client.get_channel(891403310953795605)

    if path.exists('./files/exists'):
        await channel.send("Running on PC.")
    else:
        await channel.send("Running on Heroku")

    print(f'Logged in as {client.user.name}')
    await channel.send(f'Logged in as {client.user.name}')

@client.command()
async def load(ctx, ext: str = None):
    if ext == None:
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                try:
                    client.load_extension(f'cogs.{file[:-3]}')
                    ctx.message.add_reaction('🥇')
                except: pass
    
    else:
        try:
            
            client.load_extension(f'cogs.{ext}')
            await ctx.message.add_reaction('🥇')
        except:
            await ctx.message.add_reaction('👖')

@client.command()
async def unload(ctx, ext: str = None):
    if ext == None:
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                try:
                    client.unload_extension(f'cogs.{file[:-3]}')
                    ctx.message.add_reaction('🥇')
                except: pass
    
    else:
        try:
            client.unload_extension(f'cogs.{ext}')
            
            await ctx.message.add_reaction('🥇')
        except:
            await ctx.message.add_reaction('👖')

@client.command()
async def reload(ctx, ext: str = None):
    if ext == None:
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                try:
                    client.unload_extension(f'cogs.{file[:-3]}')
                    client.load_extension(f'cogs.{file[:-3]}')
                    await ctx.message.add_reaction('🥇')
                except: pass
    
    else:
        try:
            client.unload_extension(f'cogs.{ext}')
            client.load_extension(f'cogs.{ext}')
            await ctx.message.add_reaction('🥇')
        except:
            await ctx.message.add_reaction('👖')

for i in os.listdir('./cogs'):
    if i.endswith('.py'):
        client.load_extension(f'cogs.{i[:-3]}')
        print(f'Loading {i[:-3].capitalize()}')

client.run(config.SECKEY)