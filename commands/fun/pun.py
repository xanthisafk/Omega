from requests.api import delete
import APIs.color as rang
import discord
import loggers.logger as log
import aiohttp
from discord.ext import commands
import config

class InvalidID(Exception):
    def __init__(self):
        super().__init__(f"{config.EMOTE_ERROR} Invalid ID")

class Pun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[9:]

    @commands.command(aliases=['dadjoke'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pun(self, ctx, id: str = None):

        name = 'Pun'

        headers={"Accept": "application/json", "User-Agent": "Personal discord bot: https://github.com/xanthisafk/omega"}
        if id == None:
            url = 'https://icanhazdadjoke.com/'
        else:
            url = 'https://icanhazdadjoke.com/j/' + id
        
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as r:
                f = await r.json()
                await session.close()

        if f['status'] == 404:
            raise InvalidID()

        embed = discord.Embed(title="Pun", description=f['joke'], color=await rang.get_color())
        embed.set_footer(text=f'{f["id"]} | Powered by icanhazdadjoke.com')

        await ctx.send(embed=embed)
        await log.logger(ctx, name, self.cog_name, "INFO")

    @pun.error
    async def pun_error(self, ctx, error):
        await log.logger(ctx, 'Pun', self.cog_name,"ERROR", error)
        if isinstance(error,commands.CommandOnCooldown):
            return await ctx.send(f'{config.EMOTE_ERROR} It will take {round(error.retry_after, 1)} seconds to reconnect to the **dad**abase.')
        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, InvalidID):
                return await ctx.send(f'{config.EMOTE_ERROR} Invalid ID')
        else:
            await ctx.send(f'{config.EMOTE_ERROR} An unknown error has occured.')
            raise error

def setup(client):
    client.add_cog(Pun(client))
