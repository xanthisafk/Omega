import APIs.color as rang
import discord
import aiohttp
from discord.ext import commands
import json
import codecs

class InvalidID(Exception):
    def __init__(self):
        super().__init__("Invalid ID")

class Pun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[9:]
        with codecs.open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.error_emote = config['emotes']['ERROR']
            config = None

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

        embed = discord.Embed(description=f['joke'], color=await rang.get_color())
        embed.set_footer(text=f'{f["id"]} | Powered by icanhazdadjoke.com')

        await ctx.send(embed=embed)

    @pun.error
    async def pun_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            return await ctx.send(f'{self.error_emote} It will take {round(error.retry_after, 2)} seconds to reconnect to the **dad**abase.')
        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, InvalidID):
                return await ctx.send(f'{self.error_emote} Invalid ID')
        else:
            await ctx.send(f'{self.error_emote} An unknown error has occured.')
            raise error

def setup(client):
    client.add_cog(Pun(client))
