import nextcord, aiohttp
from nextcord.ext import commands
import APIs.color as rang
import loggers.logger as log

class Panda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def panda(self, ctx, type = 'normal'):

        type = type.lower()
        
        if type == 'red':
            url = 'https://some-random-api.ml/img/red_panda'
            text = '[Here is a red panda!](https://some-random-api.ml)'
        else:
            url = 'https://some-random-api.ml/img/panda'
            text = '[Here is a panda!](https://some-random-api.ml)'

        name = 'Panda'
        color = await rang.get_color()

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                rs = await response.json()
                await session.close()
        
        embed = nextcord.Embed(description = text, color = color)
        embed.set_image(url=rs['link'])
        embed.set_footer(text='Powered by Some Random Api')
        await ctx.send(embed=embed)
        await log.logger(ctx,name,self.cog_name,'INFO')

    @panda.error
    async def pun_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            await ctx.send(f'I accidentally used black & white filter on pandas. Please wait {round(error.retry_after, 2)} seconds.')
            await log.logger(ctx,'Panda',self.cog_name,'ERROR',message=error)
            return

def setup(bot):
    bot.add_cog(Panda(bot))
