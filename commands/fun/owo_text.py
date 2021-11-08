import discord
import loggers.logger as log
import owo
from discord.ext import commands
from config import EMOTE_ERROR

class NoText(Exception):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} No text provided")

class TextTooLong(Exception):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} Text should be less than **`1800`** characters.")

class owo_text(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[9:].capitalize()

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def owoify(self, ctx, *, text: str = None):
        name = 'OwOify'
        if text == None:
            raise NoText()
        elif len(text) > 1800:
            raise TextTooLong()
        else:
            text = owo.owo(text)
            await ctx.send(text)
            await log.logger(ctx, name, self.cog_name, "INFO")

    @owoify.error
    async def owoify_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"{EMOTE_ERROR} Command is on cooldown. Try again in {round(error.retry_after,1)} seconds.")
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, NoText):
                return await ctx.send(error.original)
            elif isinstance(error.original, TextTooLong):
                return await ctx.send(error.original)
        else:
            raise error

def setup(client):
    client.add_cog(owo_text(client))
