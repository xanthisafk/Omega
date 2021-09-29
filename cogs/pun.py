import discord
from discord.ext import commands
import requests, random
import loggers.logger as log
import APIs.color as rang

class Pun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[5:].capitalize()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.cog_name} Running.')

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

            embed = discord.Embed(title = "Pun", description=f['joke'],color=await rang.get_color())
            embed.set_footer(text=f['id'])

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)
        
        except Exception as e:
            await ctx.send("Something went wrong.")
            await log.error_logger(ctx,name,self.cog_name,e)

def setup(client):
    client.add_cog(Pun(client))