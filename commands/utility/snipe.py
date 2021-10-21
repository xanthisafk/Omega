import APIs.color as rang
import discord
from discord.ext import commands

from loggers.logger import logger


class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:].capitalize()

    msg = None

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        global msg
        msg = message

    @commands.command()
    async def snipe(self, ctx):

        global msg

        color = await rang.get_color()

        try:
            thumb = msg.author.avatar_url
        except Exception as e:
            if isinstance(e, NameError):
                await ctx.send("There is nothing to snipe...")
                return

        name = msg.author.name

        embed = discord.Embed(description=msg.content, color=color)
        embed.set_author(name=name, icon_url=thumb)

        if msg.attachments == []:
            pass
        else:
            embed.set_image(url=(msg.attachments[0].url))

        await ctx.send(embed=embed)
        await logger.logger(ctx, name, self.cog_name,"INFO")


def setup(bot):
    bot.add_cog(Snipe(bot))
