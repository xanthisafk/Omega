import discord
import loggers.logger as log
import owo
from discord.ext import commands
import json
import codecs


class NoText(Exception):
    def __init__(self):
        super().__init__("No text provided")

class TextTooLong(Exception):
    def __init__(self):
        super().__init__("Text should be less than **`1800`** characters.")

class owo_text(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[9:].capitalize()
        with codecs.open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.error_emote = config['emotes']['ERROR']
            config = None

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
            return await ctx.send(f"{self.error_emote} Command is on cooldown. Try again in {round(error.retry_after,1)} seconds.")
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, NoText):
                return await ctx.send(f"{self.error_emote} Error: {error.original}")
            elif isinstance(error.original, TextTooLong):
                return await ctx.send(f"{self.error_emote} Error: {error.original}")
        else:
            raise error

def setup(client):
    client.add_cog(owo_text(client))
