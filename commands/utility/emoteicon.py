import discord
import discord
from discord.ext import commands
import APIs.color as rang



class Emoteicon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]

    @commands.command()
    async def emoji(self, ctx, emote: discord.Emoji = None):
        color = await rang.get_color()

        if emote == None:
            raise commands.MissingRequiredArgument('emoji')

        embed = discord.Embed(title=emote.name, color=color)
        embed.set_footer(text=('From: '+emote.guild.name), icon_url=emote.guild.icon_url)
        embed.set_image(url=emote.url)
        await ctx.send(embed=embed)
    
    @emoji.error
    async def emoji_error(self,ctx,error):
        if isinstance(error,commands.EmojiNotFound):
            await ctx.send(f'{error.argument} is not a valid emoji or is a default emoji.')
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(f'You need to specify an emoji.')
        else:
            await ctx.send(f"An unxpected error occured.")
            raise error

def setup(bot):
    bot.add_cog(Emoteicon(bot))
