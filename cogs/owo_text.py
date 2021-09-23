import discord
from discord.ext import commands
import owo
import loggers.logger as log

class owo_text(commands.Cog):
    cog_name = 'OwO_text'
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def owoify(self,ctx,*,text:str=None):
        name = 'OwOify'
        try:
            if text == None:
                text = owo.owo('You need to put some text for me to OwOify.')
                await ctx.send(text)
                await self.logger(name,ctx)
                return
            elif len(text) > 1800:
                text = owo.owo('Text should be less than 1800 characters.')
                await ctx.send(text)
                await self.logger(name,ctx)
                return
            else:
                text = owo.owo(text)
                await ctx.send(text)
                await log.event_logger(ctx,name,self.cog_name)
        
        except Exception as e:
                await ctx.send('Whats this? Some ewwow occuwed. XDDD')
                await log.error_logger(ctx,name,self.cog_name,e)

def setup(client):
    client.add_cog(owo_text(client))
