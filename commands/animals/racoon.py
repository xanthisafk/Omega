import nextcord, aiohttp, APIs.color as rang, loggers.logger as log
from nextcord.ext import commands


class Racoon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def racoon(self, ctx):

        name = 'Racoon'
        color = await rang.get_color()
        url = 'https://some-random-api.ml/img/racoon'
        text = '[Here is a racoon!](https://some-random-api.ml)'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                rs = await response.json()
                await session.close()
        
        embed = nextcord.Embed(description = text, color = color)
        embed.set_image(url=rs['link'])
        embed.set_footer(text='Powered by Some Random Api')
        await ctx.send(embed=embed)
        await log.logger(ctx,name,self.cog_name,'INFO')

    @racoon.error
    async def pun_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            await ctx.send(f'A racoon will be here in {round(error.retry_after, 2)} seconds.')
            await log.logger(ctx,'Racoon',self.cog_name,'ERROR',message=error)
            return

def setup(bot):
    bot.add_cog(Racoon(bot))
