import APIs.color as rang
import discord
from discord.ext import commands


class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, user: discord.Member = None):
        color = await rang.get_color()
        if user == None:
            nm = ctx.author.name + " 's avatar."
            embed = discord.Embed(title=nm, color=color)
            embed.set_image(url=ctx.author.avatar_url)

        else:
            nm = user.name + " 's avatar."
            embed = discord.Embed(title=nm, color=color)
            embed.set_image(url=user.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Avatar(bot))
