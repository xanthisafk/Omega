import discord
from discord.ext import commands
import requests, random
import loggers.logger as log

class Pun(commands.Cog):
    cog_name = 'Pun'
    def __init__(self, client):
        self.client = client

    color_list = [0xA9FBD7, 0xD7FDEC, 0xFDE74C, 0xE8DAB2, 0xDD6E42, 0xE5FCFF, 0xE5FCFF, 0xABDAFC, 0xACACDE, 0xC490D1, 0xB8336A]

    @commands.command(aliases=['dadjoke'])
    async def pun(self,ctx,id:str=None):
        name = 'Pun'

        try:
            if id == None:
                f = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json","User-Agent": "My Library"}).json()
            else:
                url = 'https://icanhazdadjoke.com/j/' + id
                f = requests.get(url, headers={"Accept": "application/json","User-Agent": "Personal discord bot: github.com/xanthisafk/coom"}).json()

            if f['status'] == 404:
                await ctx.send("❌ Invalid ID.")
                return

            embed = discord.Embed(title = "Pun", description=f['joke'],color=random.choice(self.color_list))
            embed.set_footer(text=f['id'])

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)
        
        except Exception as e:
            await ctx.send("Something went wrong.")
            await log.error_logger(ctx,name,self.cog_name,e)

def setup(client):
    client.add_cog(Pun(client))