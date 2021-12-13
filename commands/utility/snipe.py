import APIs.color as rang
import discord
from discord.ext import commands



class NothingToSnipe(Exception):
    def __init__(self):
        super().__init__("Nothing to snipe.")


class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]
        self.snip = {}
        self.before = {}


    @commands.Cog.listener()
    async def on_message_delete(self, message):

        if message.author.bot:
            return

        guildid = message.guild.id
        user = message.author.name + '#' + message.author.discriminator
        avatar = message.author.avatar_url
        content = message.content
        time = message.created_at

        self.snip.update({
            guildid: {
                "user":user,
                "avatar":avatar,
                "content":content,
                "time":time
            }
        })

    @commands.Cog.listener()
    async def on_message_edit(self, bf, at):

        if bf.author.bot or at.author.bot:
            return

        guildid = bf.guild.id
        user = bf.author.name + '#' + bf.author.discriminator
        avatar = bf.author.avatar_url
        before = bf.content
        after = at.content
        time = bf.created_at

        self.before.update({
            guildid: {
                "user":user,
                "avatar":avatar,
                "before":before,
                "after":after,
                "time":time
            }
        })

    @commands.command()
    async def snipe(self, ctx):
        if not self.snip:
            raise NothingToSnipe()

        guildid = ctx.guild.id
        try:
            user = self.snip[guildid]["user"]
        except:
            raise NothingToSnipe()
        avatar = self.snip[guildid]["avatar"]
        content = self.snip[guildid]["content"]
        time = self.snip[guildid]["time"]

        embed = discord.Embed(color = await rang.get_color(), timestamp = time)
        embed.set_author(name = user, icon_url = avatar)
        embed.description = content

        await ctx.send(embed = embed)

    @snipe.error
    async def sniped_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, NothingToSnipe):
                await ctx.send(f"{ctx.author.mention} Nothing to snipe.")
            else:
                await ctx.send(f"{ctx.author.mention} An error occured.")
                raise error
        else:
            await ctx.send(f"{ctx.author.mention} An error occured.")
            raise error

    @commands.command(name='editsnipe',aliases=['es'])
    async def snipebefore(self, ctx):
        if not self.before:
            raise NothingToSnipe()

        guildid = ctx.guild.id
        try:
            user = self.before[guildid]["user"]
        except:
            raise NothingToSnipe()
        avatar = self.before[guildid]["avatar"]
        before_content = self.before[guildid]["before"]
        after_content = self.before[guildid]["after"]
        time = self.before[guildid]["time"]

        embed = discord.Embed(color = await rang.get_color(), timestamp = time)
        embed.set_author(name = user, icon_url = avatar)
        embed.add_field(name = "Before", value = before_content, inline = False)
        embed.add_field(name = "After", value = after_content, inline = False)


        await ctx.send(embed = embed)

    @snipebefore.error
    async def snipebefore_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, NothingToSnipe):
                await ctx.send(f"{ctx.author.mention} Nothing to snipe.")
            else:
                await ctx.send(f"{ctx.author.mention} An error occured.")
                raise error
        else:
            await ctx.send(f"{ctx.author.mention} An error occured.")
            raise error

def setup(bot):
    bot.add_cog(Snipe(bot))
