import discord, os, asyncio
from discord.ext import commands
import APIs.color as rang
import loggers.logger as log

class About(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.cog_name = __name__[5:].capitalize()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.cog_name} Running.')

    @commands.command()
    async def about(self,ctx):
        command_name = ctx.command.name.capitalize()
        cog_name = ctx.command.cog_name.capitalize()

        try:
            color = await rang.get_color()

            servers = len(self.client.guilds)
            
            people = 0
            for guild in self.client.guilds:
                people += guild.member_count

            cog_amount = 0
            for i in os.listdir('./cogs'):
                cog_amount += 1
            
            command_amount = 0
            for i in self.client.commands:
                command_amount += 1

            tot_s = f'Currently in {servers} servers and working with {people} people.\n'
            tot_c = f'{command_amount+1} commands are loaded across {cog_amount} extensions.'
            field_val = tot_s+tot_c

            footer = f'Made by Xanthis for Nowhere Space!'

            thumb = self.client.user.avatar_url

            embed = discord.Embed(title='About',description='Discord bot, written in Python, uses `discord.py`',color=color)
            embed.add_field(name='Usage',value=field_val,inline=False)
            embed.set_footer(text=footer)
            embed.set_thumbnail(url=thumb)
            await ctx.send(embed=embed)
            await log.event_logger(ctx,command_name,cog_name,)
        
        except Exception as e:

            await log.error_logger(ctx,command_name,cog_name,e)
            await ctx.send('Something went wrong')



def setup(client):
    client.add_cog(About(client))