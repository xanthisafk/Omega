import nextcord
import nextcord
from nextcord.ext import commands
import APIs.color as rang
import loggers.logger as log


class Emoteicon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]

    @commands.command()
    async def emoji(self, ctx, emote: nextcord.Emoji = None):
        name = "Emoji"
        color = await rang.get_color()

        if emote == None:
            await ctx.send("Please mention an emoji")
            return

        try:

            embed = nextcord.Embed(title=emote.name, description=(f'From: {emote.guild.name}'), color=color)
            embed.set_image(url=emote.url)
            await ctx.send(embed=embed)
            await log.logger(ctx, name, self.cog_name, "INFO")
        except Exception as error:
            await log.logger(ctx, name, self.cog_name, "ERROR" ,error)
    
    @emoji.error
    async def emoji_error(self,ctx,error):
        if isinstance(error,commands.EmojiNotFound):
            await ctx.send(f'{error.argument} is not a valid emoji.')
            await log.logger(ctx, 'Emoji', self.cog_name, "ERROR" ,error)
        else:
            await log.logger(ctx, 'Emoji', self.cog_name, "ERROR" ,error)
            raise error

def setup(bot):
    bot.add_cog(Emoteicon(bot))
