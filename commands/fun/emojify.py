import json
import codecs

import discord
from discord.ext import commands
from emojifier import Emojifier

class NoText(Exception):
    def __init__(self):
        super().__init__("Give me some text to work with!")

class TextTooBig(Exception):
    def __init__(self):
        super().__init__("Maximum 1500 characters only.\nText you gave is too big!")

class Emoji(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[9:].capitalize()
        with codecs.open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.error_emote = config['emotes']['ERROR']
            config = None


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

    @emojify.error
    async def emojify_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f'{self.error_emote}  You are on cooldown! Try again in {round(error.retry_after,2)} seconds.')

        elif isinstance(error.original, NoText):
            await ctx.reply(f"{self.error_emote} Error: {error.original}")

        elif isinstance(error.original, TextTooBig):
            await ctx.reply(f"{self.error_emote} Error: {error.original}")

        else:
            await ctx.send(f'{self.error_emote} An error occured.')
            raise error





def setup(client):
    client.add_cog(Emoji(client))
