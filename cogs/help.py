import discord
from discord.ext import commands
import random, json, codecs
import loggers.logger as log
import APIs.color as rang

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[5:].capitalize()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.cog_name} Running.')

    
    title = 'Bot for ***Nowhere Space***.'
    postfix = '\nUse `>help <command>` for more information.'
    flair = title+postfix

    emotes = "`Blush`, `Dance`, `Wave`, `Sleep`, `Vibe`, `Pat`, `Cry`, `Pout`, `Kiss`, `Bully`, `Cuddle`, `Hug`, `Lick`, `Smug`, `Bonk`, `Yeet`, `Smile`, `Highfive`, `Handhold`, `Eat`, `Bite`, `Glomp`, `Slap`, `Kill`, `Kick`, `Wink`, `Poke`, `Cringe`"

    fun = """
    `emojify`, `owoify`, `pun`
    """

    general = '__*General*__: `status`'
    fat = '\n__*For auto trigger*__: `ignore`, `unignore`, `add_atk`, `remove_atk`'
    utility = general + fat

    atka = 'List all Auto Trigger Keywords using `>help atk`'

    @commands.group(invoke_without_command=True)
    async def help(self,ctx):
        name = 'Help'

        color = await rang.get_color()
        embed = discord.Embed(title='Help dialogue', description=self.flair,color=color)
        embed.add_field(name='Emotes', value = self.emotes, inline=False)
        embed.add_field(name='Fun',value=self.fun,inline=False)
        embed.add_field(name='Auto trigger keywords', value = self.atka, inline=False)
        embed.add_field(name='Utility',value=self.utility,inline=False)
        if random.choice(range(1,100)) == 69:
            embed.set_footer(text='Made by Xanthis')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

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
    async def emotes(self,ctx):
        try:
            name = ctx.invoked_with
            color = await rang.get_color()
            with codecs.open('./files/emote-help.json', 'r', encoding='utf-8') as js:
                data = json.load(js)
                js.close()
            
            desc = data[name]['desc'] + '\nAliases: ' + data[name]['alis']
            synt = '`' + data[name]['synt'] + '`'
            
            if data[name]['opti'] == 0:
                footer = 'Argument is <required>'
            elif data[name]['opti'] == 1:
                footer = 'Argument is [optional]'
            else:
                footer = "No arguments"
            
            embed = discord.Embed(title=name.capitalize(),description=desc,color=color)
            embed.add_field(name='Syntax', value=synt)
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
            await log.event_logger(ctx,name.capitalize(),self.cog_name)
        
        except Exception as e:
            print(e)
            await ctx.send('Something went VERY wrong.')
            await log.error_logger(ctx,name.capitalize(),self.cog_name,e)

    ############################
    # UTILITY COG HELP SECTION #
    ############################

    @help.command()
    async def ignore(self,ctx):
        name = 'Ignore'
        color = await rang.get_color()
        embed = discord.Embed(title='Ignore', description='Disable bot auto trigger words for you',color=color)
        embed.add_field(name='Syntax',value='`>ignore`')
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command()
    async def unignore(self,ctx):
        name = 'Unignore'
        color = await rang.get_color()
        embed = discord.Embed(title='Ignore', description='Enable bot auto trigger words for you',color=color)
        embed.add_field(name='Syntax',value='`>unignore`')
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command(aliases=['ping'])
    async def status(self,ctx):
        name = 'Status'
        color = await rang.get_color()
        embed = discord.Embed(title='Status', description='Checks the bot connection and Discord API status.\nAliases: `ping`',color=color)
        embed.add_field(name='Syntax',value='`>status`')
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)
    
    @help.command()
    async def add_atk(self,ctx):
        name = 'Add Auto Trigger Keyword'
        color = await rang.get_color()
        text = 'Adds an Auto Trigger Keyword (ATK) to list. This can then be called by anyone.\nRequires administration privilage.'
        syntax = '`>add_atk <trigger word, value>`\nTrigger word is the word that triggers the bot.\nValue is what will be sent by bot after being triggerd.\nComma between them is required. Only 1 comma is allowed.'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)
    
    @help.command()
    async def remove_atk(self,ctx):
        name = 'Remove Auto Trigger Keyword'
        color = await rang.get_color()
        text = 'Removes an Auto Trigger Keyword (ATK) from the list.\nRequires administration privilage.'
        syntax = '`>add_atk <trigger word>`\nTo list all ATKs, use `>help atk`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)
    
    #################################
    # AUTO TRIGGER COG HELP SECTION #
    #################################

    @help.command()
    async def atk(self,ctx):
        name = 'Auto Trigger Keywords'
        color = await rang.get_color()
        text = 'Auto Trigger Keywords trigger the bot to post a message instantly when sent in chat.'
        syntax = ''
        with open('files/list.json', "r") as js:
            data = json.load(js)
            js.close()

        temp = []
        for i in data:
            temp.append(i)

        temp.sort(key=str.lower)

        for i in temp:
            syntax += f'`{i}`, '
        syntax = syntax[:-2]

        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)


def setup(client):
    client.add_cog(Help(client))