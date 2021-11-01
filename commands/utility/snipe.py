import APIs.color as rang
import discord
from discord.ext import commands

from loggers.logger import logger


class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]

    msg = ''
    before = ''
    after = ''


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        
        global msg
        msg = message

    @commands.Cog.listener()
    async def on_message_edit(self, bf, at):

        global before
        global after
        before = bf
        after = at

    @commands.command()
    async def snipe(self, ctx):
        global msg
        color = await rang.get_color()
        
        if msg == None:
            return await ctx.send('No message to snipe!')
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
        await logger(ctx, 'snipe', self.cog_name,"INFO")

    @commands.command(aliases=['es'])
    async def editsnipe(self, ctx):
        global before, after
        try:
            thumb = before.author.avatar_url
        except Exception as e:
            if isinstance(e, NameError):
                return await ctx.send("There is nothing to snipe...")

        name = before.author.name

        embed = discord.Embed(color=await rang.get_color())
        embed.set_author(name=name, icon_url=thumb)

        embed.add_field(name="Before", value=before.content)
        embed.add_field(name="After", value=after.content, inline=False)

        await ctx.send(embed=embed)
        return await logger(ctx, 'editsnipe', self.cog_name,"INFO")


def setup(bot):
    bot.add_cog(Snipe(bot))
