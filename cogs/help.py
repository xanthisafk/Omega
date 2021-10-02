import discord
from discord.ext import commands
import random, json, codecs
import loggers.logger as log
import APIs.color as rang

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[5:].capitalize()


    async def emo_section(self):
        syntax = ''
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

        with codecs.open('files/emote-help.json','r',encoding='utf-8') as js:
            data = json.load(js)
            js.close()

        syntax = ''

        for i in data['utility']:
            syntax += f'`{i}`, '
        syntax = syntax[:-2]

        return syntax

    async def fun_section(self):

        with codecs.open('files/emote-help.json','r',encoding='utf-8') as js:
            data = json.load(js)
            js.close()

        syntax = ''

        for i in data['fun']:
            syntax += f'`{i}`, '
        syntax = syntax[:-2]

        return syntax

    @commands.group(invoke_without_command=True)
    async def help(self,ctx):

        name = 'Help'

        emo = await self.emo_section()
        fun = await self.fun_section()
        uti = await self.uti_section()
        atk = 'List all Auto Trigger Keywords using `>help atk`'
        hdr = 'Bot for ***Nowhere Space***.\nUse `>help <command>` for more information.'
        

        color = await rang.get_color()

        embed = discord.Embed(title = 'Help dialogue', description = hdr, color = color)
        embed.add_field(name='Emotes', value = emo, inline = False)
        embed.add_field(name='Fun', value = fun, inline = False)
        embed.add_field(name='Auto trigger keywords', value = atk, inline = False)
        embed.add_field(name='Utility', value = uti, inline = False)

        if random.choice(range(1,100)) == 69:
            embed.set_footer(text = 'Made by Xanthis')

        await ctx.send(embed = embed)
        await log.event_logger(ctx, name, self.cog_name)

    ############################
    # EMOTES COG HELP SECTION  #
    ############################

    @help.command(aliases=[
        'blush',    'kiss',     'smile',    'bite',     'poke',
        'dance',    'bully',    'throw',    'nom',      'cringe',
        'wave',     'cuddle',   'happy',    'glomp',
        'sleep',    'hug',      'highfive', 'superhug',
        'vibe',     'lick',     'handhold', 'slap',
        'pat',      'smug',     'hold',     'kill',
        'cry',      'bonk',     'eat', '    kick',
        'pout',     'yeet',     'hungry',   'wink'
    ])
    async def emotes_help(self,ctx):
        """
        Sends out help embed for every element in emotes in emote-help.json
        There are a lot of these. I feel stupid for handwriting all that before now.
        """
        try:
            name = ctx.invoked_with
            color = await rang.get_color()
            with codecs.open('./files/emote-help.json', 'r', encoding='utf-8') as js:
                data = json.load(js)
                js.close()
            
            desc = data['emotes'][name]['desc'] + '\nAliases: ' + data['emotes'][name]['alis']
            synt = '`' + data['emotes'][name]['synt'] + '`'
            
            if data['emotes'][name]['opti'] == 0:
                footer = 'Argument is <required>'
            elif data['emotes'][name]['opti'] == 1:
                footer = 'Argument is [optional]'
            else:
                footer = "No arguments"
            
            embed = discord.Embed(title=name.capitalize(),description=desc,color=color)
            embed.add_field(name='Syntax', value=synt)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
            await log.event_logger(ctx,name.capitalize(),self.cog_name)
        
        except Exception as e:
            await ctx.send('Something went VERY wrong.')
            await log.error_logger(ctx,name.capitalize(),self.cog_name,e)
            raise e
    

    ########################
    # FUN COG HELP SECTION #
    ########################

    @help.command(aliases=[
        'emojify', 'owoify',
        'pun', 'dadjoke'
    ])
    async def fun_help(self,ctx):
        """
        Sends out help embed for every element in fun in emote-help.json
        """
        try:
            name = ctx.invoked_with
            color = await rang.get_color()
            with codecs.open('./files/emote-help.json', 'r', encoding='utf-8') as js:
                data = json.load(js)
                js.close()
            
            desc = data['fun'][name]['desc'] + '\nAliases: ' + data['fun'][name]['alis']
            synt = '`' + data['fun'][name]['synt'] + '`'
            
            if data['fun'][name]['opti'] == 0:
                footer = 'Argument is <required>'
            elif data['fun'][name]['opti'] == 1:
                footer = 'Argument is [optional]'
            else:
                footer = "No arguments"
            
            embed = discord.Embed(title=name.capitalize(),description=desc,color=color)
            embed.add_field(name='Syntax', value=synt)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
            await log.event_logger(ctx,name.capitalize(),self.cog_name)
        
        except Exception as e:
            await ctx.send('Something went VERY wrong.')
            await log.error_logger(ctx,name.capitalize(),self.cog_name,e)
            raise e

    ############################
    # UTILITY COG HELP SECTION #
    ############################

    @help.command(aliases=[
        'ignore', 'uignore', 'add_atk', 'remove_atk',
        'atk_add', 'atk_remove', 'status', 'ping'
    ])
    async def utility_help(self,ctx):
        """
        Sends out help embed for every element in utility in emote-help.json
        """
        try:
            name = ctx.invoked_with
            color = await rang.get_color()
            with codecs.open('./files/emote-help.json', 'r', encoding='utf-8') as js:
                data = json.load(js)
                js.close()
            
            desc = data['utility'][name]['desc'] + '\nAliases: ' + data['utility'][name]['alis']
            synt = '`' + data['utility'][name]['synt'] + '`'
            
            if data['utility'][name]['opti'] == 0:
                footer = 'Argument is <required>'
            elif data['utility'][name]['opti'] == 1:
                footer = 'Argument is [optional]'
            else:
                footer = "No arguments"
            
            embed = discord.Embed(title=name.capitalize(),description=desc,color=color)
            embed.add_field(name='Syntax', value=synt)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
            await log.event_logger(ctx,name.capitalize(),self.cog_name)
        
        except Exception as e:
            await ctx.send('Something went VERY wrong.')
            await log.error_logger(ctx,name.capitalize(),self.cog_name,e)
            raise e
    
    #################################
    # AUTO TRIGGER COG HELP SECTION #
    #################################

    @help.command(name='atk')
    async def atk_help(self,ctx):
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
        for i in data:
            temp.append(i)

        temp.sort(key=str.lower)

        for i in temp:
            syntax += f'`{i}`, '
        syntax = syntax[:-2]

        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    # @commands.command()
    # async def testin(self, ctx):
    #     if ctx.author.id == 800400638156210176:
    #         cog = self.client.get_cog('Emotes')
    #         syntax =''
    #         name = cog.get_commands()
    #         for i in name:
    #             for j in i.aliases:
    #                 syntax += f'`{j}`, '
    #             syntax += f'`{i.name}`'
    #         print(syntax)

def setup(client):
    client.add_cog(Help(client))