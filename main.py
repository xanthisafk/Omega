import discord
from discord.ext import commands
import config
import os

intents = discord.Intents(messages=True,members=True,emojis=True)
client = commands.Bot(command_prefix = config.PREFIX, case_insensitive = True, intents = intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

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

client.run(config.SECKEY)