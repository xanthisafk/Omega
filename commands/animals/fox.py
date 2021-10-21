import discord, aiohttp, APIs.color as rang, loggers.logger as log
from discord.ext import commands


class Fox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fox(self, ctx):

        name = 'Fox'
        color = await rang.get_color()
        
        async with aiohttp.ClientSession() as session:
            async with session.get('https://randomfox.ca/floof') as response:
                res = await response.json()
                url = res['image']
                await session.close()

        embed = discord.Embed(description='[A fox image for you](https://randomfox.ca/)',color=color)
        embed.set_image(url=url)
        embed.set_footer(text='Powered by randomfox.ca')
        await ctx.send(embed=embed)
        await log.logger(ctx,name,self.cog_name,'INFO')

    @fox.error
    async def pun_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            await ctx.send(f'Foxes are rare. Please wait {round(error.retry_after, 2)} seconds.')
            await log.logger(ctx,'Fox',self.cog_name,'ERROR',message=error)
            return

def setup(bot):
    bot.add_cog(Fox(bot))
