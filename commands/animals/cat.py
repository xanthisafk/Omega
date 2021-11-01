import discord, aiohttp, APIs.color as rang, random, loggers.logger as log
from discord.ext import commands


class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]

    @commands.command(aliases=["meow","purr","kitty"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cat(self, ctx):

        name = 'Cat'
        color = await rang.get_color()

        url = 'https://aws.random.cat/meow'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                js = await response.json()
                await session.close()

        embed=discord.Embed(description=f'[me{"o"*random.randint(1,10)}w](https://aws.random.cat/meow)',color=color)
        embed.set_image(url=js['file'])
        embed.set_footer(text='Powered by random.cat')
        await ctx.send(embed = embed)
        await log.logger(ctx,name,self.cog_name,'INFO')

    @cat.error
    async def pun_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            await ctx.send(f'To find a purr-fect photo of cat, it will take me {round(error.retry_after, 2)} seconds.')
            await log.logger(ctx,'Cat',self.cog_name,'ERROR',message=error)
            return

def setup(bot):
    bot.add_cog(Cat(bot))
