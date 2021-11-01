from requests.api import delete
import APIs.color as rang
import discord
import loggers.logger as log
import aiohttp
from discord.ext import commands
import config


class Pun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[9:].capitalize()

    @commands.command(aliases=['dadjoke'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pun(self, ctx, id: str = None):

        name = 'Pun'

        try:
            headers={"Accept": "application/json", "User-Agent": "Personal discord bot: github.com/xanthisafk/omega"}
            if id == None:
                url = 'https://icanhazdadjoke.com/'
            else:
                url = 'https://icanhazdadjoke.com/j/' + id
            
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as r:
                    f = await r.json()
                    await session.close()

            if f['status'] == 404:
                await ctx.send(f"{config.EMOTE_ERROR} Invalid ID.")
                return

            embed = discord.Embed(title="Pun", description=f['joke'], color=await rang.get_color())
            embed.set_footer(text=f['id'])

            await ctx.send(embed=embed)
            await log.logger(ctx, name, self.cog_name, "INFO")

        except Exception as e:
            await ctx.send("Something went wrong.")
            await log.logger(ctx, name, self.cog_name,"ERROR", e)
            raise e

    @pun.error
    async def pun_error(self, ctx, error):
        await log.logger(ctx, 'Pun', self.cog_name,"ERROR", error)
        if isinstance(error,commands.CommandOnCooldown):
            await ctx.send(f'It will take {round(error.retry_after, 2)} seconds to reconnect to the **dad** abase.')
            return

def setup(client):
    client.add_cog(Pun(client))
