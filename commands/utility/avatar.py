import APIs.color as rang
import discord
from discord.ext import commands

import codecs
import json


class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]
        with codecs.open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.error_emote = config['emotes']['ERROR']
            config = None

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, user:discord.Member = None):
        color = await rang.get_color()
        print("Check")
        if user == None or not isinstance(user, discord.Member):
            nm = ctx.author.name + " 's avatar."
            av = ctx.author.avatar_url
            print(1, av)
            embed = discord.Embed(title=nm, color=color)
            embed.set_image(url=av)

        else:
            nm = user.name + "'s avatar."
            av = user.avatar_url
            print(2, av)
            embed = discord.Embed(title=nm, color=color)
            embed.set_image(url=av)

        await ctx.send(embed=embed)

    @avatar.error
    async def avatar_error(self, ctx, error):
        await ctx.send(f"{self.error_emote} An unxpected error occured")
        raise error


def setup(bot):
    bot.add_cog(Avatar(bot))
