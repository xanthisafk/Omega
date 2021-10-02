import discord
from discord.ext import commands
import random, requests, json, codecs
import loggers.logger as log
import APIs.color as rang
import APIs.GIF_And_Text

class Emotes(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[5:].capitalize()
        self.gif = APIs.GIF_And_Text.GIF_And_Text()

    @commands.command(name='hungry', aliases=[
        'blush',    'kiss',     'smile',    'bite',
        'bully',    'throw',    'nom',      'cringe',
        'wave',     'cuddle',   'happy',    'glomp',
        'hug',      'highfive', 'superhug', 'poke',
        'lick',     'handhold', 'slap',     'wink',
        'pat',      'smug',     'hold',     'kill',
        'cry',      'bonk',     'eat',      'kick',
        'yeet',     'dance',    'sleep',    'vibe',
        'pout'
    ])
    async def send_emotes_waifu(self, ctx, member:discord.Member=None):
        
        name = ctx.invoked_with
        color = await rang.get_color()

        with codecs.open('files/emote-help.json', 'r', encoding='utf-8') as js:
            alias = json.load(js)
            js.close()

        if member is None:
            if alias['emotes'][name]['opti'] == 0:
                await ctx.send(alias['emotes'][name]['erro'])
                return
            else:
                solo = True
        else:
            solo = False

        alias = None

        u1 = ctx.author.name

        if not solo:
            u2 = member.name
            string = await self.gif.create_string(type=name,user1=u1,user2=u2)
        else:
            string = await self.gif.create_string(type=name,user1=u1)

        image = await self.gif.selector(name)

        embed = discord.Embed(title = string, color = color)
        embed.set_image(url=image)
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

def setup(client):
    client.add_cog(Emotes(client))
