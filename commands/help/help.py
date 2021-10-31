import asyncio
import codecs
import json
import random

import APIs.color as rang
import nextcord
import loggers.logger as log
from nextcord.ext import commands
import config


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[9:].capitalize()

    async def emo_section(self):
        syntax = ""
        temp = []

        cog = self.client.get_cog('Emotes')
        cmd = cog.get_commands()
        for i in cmd:
            for j in i.aliases:
                temp.append(j)
            temp.append(i.name)

        temp.sort(key=str.lower)

        for i in temp:
            syntax += f'`{i}`, '
        syntax = syntax[:-2]
        return syntax

    async def uti_section(self):

        with codecs.open('files/help.json', 'r', encoding='utf-8') as js:
            data = json.load(js)
            js.close()

        syntax = ''

        for i in data['utility']:
            syntax += f'`{i}`, '
        syntax = syntax[:-2]

        return syntax

    async def fun_section(self):

        with codecs.open('files/help.json', 'r', encoding='utf-8') as js:
            data = json.load(js)
            js.close()

        syntax = ''

        for i in data['fun']:
            syntax += f'`{i}`, '
        syntax = syntax[:-2]

        return syntax
    
    async def paw_section(self):

        with codecs.open('files/help.json', 'r', encoding='utf-8') as js:
            data = json.load(js)
            js.close()

        syntax = ''

        for i in data['animals']:
            syntax += f'`{i}`, '
        syntax = syntax[:-2]

        return syntax

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):

        name = 'Help'

        emo = await self.emo_section()
        fun = await self.fun_section()
        uti = await self.uti_section()
        paw = await self.paw_section()
        atk = 'List all Auto Trigger Keywords using `>help atk`'
        hdr = 'Bot for ***Nowhere Space***.\nUse `>help <command>` for more information.'

        color = await rang.get_color()

        embed = nextcord.Embed(title='Help dialogue',
                              description=hdr, color=color)
        embed.add_field(name='Emotes', value=emo, inline=False)
        embed.add_field(name='Fun', value=fun, inline=False)
        embed.add_field(name='Animals', value=paw, inline=False)
        embed.add_field(name='Auto trigger keywords', value=atk, inline=False)
        embed.add_field(name='Utility', value=uti, inline=False)

        if random.choice(range(1, 100)) == 50:
            embed.set_footer(text='Made by Xanthis')

        await ctx.send(embed=embed)
        await log.logger(ctx, name, self.cog_name,"INFO")

    ############################
    # EMOTES COG HELP SECTION  #
    ############################

    @help.command(aliases=['blush', 'dance', 'wave', 'sleep', 'vibe', 'pat', 'cry', 'pout', 'kiss', 'bully', 'hug', 'cuddle', 'lick', 'smug', 'bonk', 'yeet', 'throw', 'smile', 'happy', 'highfive', 'handhold', 'hold', 'eat', 'hungry', 'bite', 'glomp', 'superhug', 'slap', 'kill', 'kick', 'wink', 'poke', 'cringe', 'baka', 'hmph', 'bored', 'facepalm', 'feed', 'laugh', 'shrug', 'stare', 'think', 'thonk', 'thumbsup', 'tickle', 'run'])
    async def emotes_help(self, ctx):
        """
        Sends out help embed for every element in emotes in help.json
        There are a lot of these. I feel stupid for handwriting all that before now.

        """
        try:
            name = ctx.invoked_with
            color = await rang.get_color()
            with codecs.open('./files/help.json', 'r', encoding='utf-8') as js:
                data = json.load(js)
                js.close()

            desc = data['emotes'][name]['desc'] + \
                '\nAliases: ' + data['emotes'][name]['alis']
            synt = '`' + data['emotes'][name]['synt'] + '`'

            if data['emotes'][name]['opti'] == 0:
                footer = 'Argument is <required>'
            elif data['emotes'][name]['opti'] == 1:
                footer = 'Argument is [optional]'
            else:
                footer = "No arguments"

            embed = nextcord.Embed(title=name.capitalize(),
                                  description=desc, color=color)
            embed.add_field(name='Syntax', value=synt)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
            await log.logger(ctx, name, self.cog_name,"INFO")

        except Exception as e:
            await ctx.send(f'{config.EMOTE_ERROR} Something went wrong.')
            await log.logger(ctx, name.capitalize(), self.cog_name,"ERROR", e)
            raise e

    ########################
    # FUN COG HELP SECTION #
    ########################

    @help.command(aliases=[
        'emojify', 'owoify',
        'pun', 'dadjoke', '8ball', 'gtn'
    ])
    async def fun_help(self, ctx):
        """
        Sends out help embed for every element in fun in help.json
        """
        try:
            name = ctx.invoked_with
            color = await rang.get_color()
            with codecs.open('./files/help.json', 'r', encoding='utf-8') as js:
                data = json.load(js)
                js.close()

            desc = data['fun'][name]['desc'] + \
                '\nAliases: ' + data['fun'][name]['alis']
            synt = '`' + data['fun'][name]['synt'] + '`'

            if data['fun'][name]['opti'] == 0:
                footer = 'Argument is <required>'
            elif data['fun'][name]['opti'] == 1:
                footer = 'Argument is [optional]'
            else:
                footer = "No arguments"

            embed = nextcord.Embed(title=name.capitalize(),
                                  description=desc, color=color)
            embed.add_field(name='Syntax', value=synt)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
            await log.logger(ctx, name, self.cog_name,"INFO")

        except Exception as e:
            await ctx.send('Something went VERY wrong.')
            await log.logger(ctx, name, self.cog_name,"ERROR", e)
            raise e

    ############################
    # UTILITY COG HELP SECTION #
    ############################

    @help.command(aliases=[
        'ignore', 'uignore', 'add_atk', 'remove_atk',
        'atk_add', 'atk_remove', 'status', 'ping', 'snipe', 'avatar', 'av'
    ])
    async def utility_help(self, ctx):
        """
        Sends out help embed for every element in utility in help.json
        """
        try:
            name = ctx.invoked_with
            color = await rang.get_color()
            with codecs.open('./files/help.json', 'r', encoding='utf-8') as js:
                data = json.load(js)
                js.close()

            desc = data['utility'][name]['desc'] + \
                '\nAliases: ' + data['utility'][name]['alis']
            synt = '`' + data['utility'][name]['synt'] + '`'

            if data['utility'][name]['opti'] == 0:
                footer = 'Argument is <required>'
            elif data['utility'][name]['opti'] == 1:
                footer = 'Argument is [optional]'
            else:
                footer = "No arguments"

            embed = nextcord.Embed(title=name.capitalize(),
                                  description=desc, color=color)
            embed.add_field(name='Syntax', value=synt)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
            await log.logger(ctx, name, self.cog_name,"INFO")

        except Exception as e:
            await ctx.send('Something went VERY wrong.')
            await log.logger(ctx, name, self.cog_name,"ERROR", e)
            raise e

    #################################
    # AUTO TRIGGER COG HELP SECTION #
    #################################

    @help.command(name='atk')
    async def atk_help(self, ctx):
        """
        Sends out a help embed listing all the available auto trigger keywords.
        """
        name = 'Auto Trigger Keywords'
        color = await rang.get_color()
        text = 'Auto Trigger Keywords trigger the bot to post a message instantly when sent in chat.'
        syntax = ''
        cog = self.client.get_cog('ATK')
        data = cog.atks

        temp = []
        synt = []
        for i in data:
            temp.append(i)

        temp.sort(key=str.lower)

        for i in temp:
            syntax += f'`{i}`, '
            if len(syntax) >= 1000:
                syntax = syntax[:-2]
                synt.append(syntax)
                syntax = ''

            if i == temp[(len(temp)-1)]:
                syntax = syntax[:-2]
                synt.append(syntax)
                syntax = ''

        i = 0
        page = 1
        total_pages = len(synt)

        embed = nextcord.Embed(title=name, description=text, color=color)

        embed.add_field(
            name=f'Syntax (Page {page}):', value=synt[i], inline=False)

        message = await ctx.send(embed=embed)
        embed = None

        # https://stackoverflow.com/a/61793587/14504836
        if len(synt) >= 2:
            right_e = config.EMOTE_RIGHT
            left_e = config.EMOTE_LEFT
            await message.add_reaction(left_e)
            await message.add_reaction(right_e)

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in [left_e, right_e]

            while True:
                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=120, check=check)

                    embed = nextcord.Embed(
                        title=name, description=text, color=color)

                    if str(reaction.emoji) == right_e and page != total_pages:
                        page += 1
                        embed.add_field(
                            name=f'Syntax (Page {page}):', value=synt[(page-1)], inline=False)
                        await message.edit(embed=embed)
                        await message.remove_reaction(reaction, user)

                    elif str(reaction.emoji) == left_e and page > 1:
                        page -= 1
                        embed.add_field(
                            name=f'Syntax (Page {page}):', value=synt[(page-1)], inline=False)
                        await message.edit(embed=embed)
                        await message.remove_reaction(reaction, user)

                    else:
                        await message.remove_reaction(reaction, user)

                except asyncio.TimeoutError:
                    await message.clear_reaction(right_e)
                    await message.clear_reaction(left_e)
                    await message.edit(content="Message timed out")
                    break

        await log.logger(ctx, name, self.cog_name,"INFO")

    ############################
    # ANIMALS COG HELP SECTION #
    ############################

    @help.command(aliases=['cat','dog','fox', 'bird', 'duck', 'koala', 'panda', 'racoon'])
    async def animal_help(self, ctx):
        try:
            name = ctx.invoked_with
            color = await rang.get_color()
            with codecs.open('./files/help.json', 'r', encoding='utf-8') as js:
                data = json.load(js)
                js.close()

            desc = data['animals'][name]['desc'] + \
                '\nAliases: ' + data['animals'][name]['alis']
            synt = '`' + data['animals'][name]['synt'] + '`'

            if data['animals'][name]['opti'] == 0:
                footer = 'Argument is <required>'
            elif data['animals'][name]['opti'] == 1:
                footer = 'Argument is [optional]'
            else:
                footer = "No arguments"

            embed = nextcord.Embed(title=name.capitalize(),
                                  description=desc, color=color)
            embed.add_field(name='Syntax', value=synt)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
            await log.logger(ctx, name, self.cog_name,"INFO")

        except Exception as e:
            await ctx.send('Something went VERY wrong.')
            await log.logger(ctx, name, self.cog_name,"ERROR", e)
            raise e
        

    @commands.command()
    async def testin(self, ctx):
        if ctx.author.id == 800400638156210176:
            emoji = self.client.emojis
            for i in emoji:
               print(i)
            await ctx.send('<:ok:899558562819358720>')


def setup(client):
    client.add_cog(Help(client))
