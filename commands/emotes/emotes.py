import codecs
import json
from typing import Union

import APIs.color as rang
import APIs.emotehelper
import discord
import loggers.logger as log
from discord.ext import commands


class Emotes(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[9:].capitalize()
        self.gif = APIs.emotehelper.GIF_And_Text()

    aliases = ['dance', 'wave', 'sleep', 'vibe', 'pat', 'cry', 'pout', 'kiss', 'bully', 'hug', 'cuddle', 'lick', 'smug', 'bonk', 'yeet', 'throw', 'smile', 'happy', 'highfive', 'handhold', 'hold', 'eat',
               'hungry', 'bite', 'glomp', 'superhug', 'slap', 'kill', 'kick', 'wink', 'poke', 'cringe', 'baka', 'hmph', 'bored', 'facepalm', 'feed', 'laugh', 'shrug', 'stare', 'think', 'thonk', 'thumbsup', 'tickle', 'run']

    @commands.command(name='blush', aliases=aliases)
    async def send_emotes(self, ctx, member: Union[discord.Member, str] = None):
        """
        Sends an embeded GIF file based on the chosen category.

        args:
            ctx: disocrd.Context
            member: discord.Member / str -> Mentioned user. If not provided where it is needed, an error message is sent. If member is str then it is considered solo.
        """

        # String that was used to invoke this command. It is used to gather information from files/help.json
        name = ctx.invoked_with.lower()
        # A random hex color for embed
        color = await rang.get_color()

        # Loads the json data to memory
        with codecs.open('files/help.json', 'r', encoding='utf-8') as js:
            alias = json.load(js)
            js.close()

        # If no member is mentioned or member is a string
        if member == None or isinstance(member,str):
            
            # Checks if a member being mentioned is required.
            if alias['emotes'][name]['opti'] == 0:
                await ctx.send(alias['emotes'][name]['erro'])
                return

            else:
                solo = True

        else:
            solo = False

        # Gets category from json data.
        category = alias['emotes'][name]['cate']

        # Clears memory?
        alias = None

        # Author name (user1)
        u1 = ctx.author.name

        # If command is not solo
        if not solo:

            # Mentioned user name (user2)
            u2 = member.name

            # Gets a string from APIs/GIF_And_Text.py for specified type that involves 2 users
            string = await self.gif.create_string(type=name, user1=u1, user2=u2)

        else:
            # Gets a string from APIs/GIF_And_Text.py for specified type for 1 user
            string = await self.gif.create_string(type=name, user1=u1)

        # Gets an image for specified type from APIs/emotes.py
        image = await self.gif.selector(category)

        # Create and send the embed. Log the use of this command.
        embed = discord.Embed(title=string, color=color)
        embed.set_image(url=image)
        await ctx.send(embed=embed)
        await log.logger(ctx,name,self.cog_name,'INFO')


def setup(client):
    client.add_cog(Emotes(client))
