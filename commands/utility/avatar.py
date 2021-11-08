import APIs.color as rang
import discord
from discord.ext import commands

from loggers.logger import logger


class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, user = None):
        color = await rang.get_color()
        if user == None or not isinstance(user, discord.Member):
            nm = ctx.author.name + " 's avatar."
            embed = discord.Embed(title=nm, color=color)
            embed.set_image(url=ctx.author.avatar_url)

        else:
            nm = user.name + "'s avatar."
            embed = discord.Embed(title=nm, color=color)
            embed.set_image(url=user.avatar_url)

    @avatar.error
    async def avatar_error(self, ctx, error):
        await ctx.send("An unxpected error occured")
        raise error

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Avatar(bot))
