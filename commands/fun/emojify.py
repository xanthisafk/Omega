import json

import discord
import loggers.logger as log
from discord.ext import commands
from emojifier import Emojifier
import config

class NoText(Exception):
    def __init__(self):
        super().__init__(f"{config.EMOTE_ERROR} Give me some text to work with!")

class TextTooBig(Exception):
    def __init__(self):
        super().__init__(f"{config.EMOTE_ERROR} Maximum 1500 characters only.\nText you gave is too big!")

class Emoji(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[9:].capitalize()


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def emojify(self, ctx, *, text=None):
        name = 'Emojify'

    
        # Loads the emoji-mappings.json file
        with open("files/emoji-mappings.json", "r", encoding="utf8") as f:
            mapping = json.load(f)
        emoji = Emojifier.of_custom_mappings(mapping)

        # Checks if no text was given
        if text == None:
            raise NoText()

        # Checks if length of given text is less than 1500
        elif len(text) > 1500:
            raise TextTooBig()

            # Runs the actual code if both test cases pass
        else:
            text = emoji.generate_emojipasta(text)
            await ctx.send(text)
            await log.logger(ctx, name, self.cog_name, "INFO")

    @emojify.error
    async def emojify_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f'{config.EMOTE_ERROR}  You are on cooldown! Try again in {round(error.retry_after,1)} seconds.')

        elif isinstance(error.original, NoText):
            await ctx.reply(error.original)

        elif isinstance(error.original, TextTooBig):
            await ctx.reply(error.original)

        else:
            await ctx.send(f'{config.EMOTE_ERROR} An error occured.')
            raise error





def setup(client):
    client.add_cog(Emoji(client))
