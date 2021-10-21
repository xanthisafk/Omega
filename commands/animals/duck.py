import discord, aiohttp, APIs.color as rang, loggers.logger as log
from discord.ext import commands


class Duck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]


    @commands.command(aliases=['quuck','quacc'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def duck(self, ctx):

        name = 'Duck'
        color = await rang.get_color()

        async with aiohttp.ClientSession() as session:
            async with session.get('https://random-d.uk/api/v2/random') as response:
                res = await response.json()
                await session.close()
        
        embed = discord.Embed(description='[Here is a random duck](https://random-d.uk/)', color = color)
        embed.set_image(url=res['url'])
        embed.set_footer(text=res['message'])
        await ctx.send(embed=embed)
        await log.logger(ctx,name,self.cog_name,'INFO')
    
    @duck.error
    async def pun_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            await ctx.send(f'Too many quacks. Please wait {round(error.retry_after, 2)} seconds.')
            await log.logger(ctx,'Duck',self.cog_name,'ERROR',message=error)
            return


def setup(bot):
    bot.add_cog(Duck(bot))
