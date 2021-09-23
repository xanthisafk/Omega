import discord
from discord.ext import commands
import random, json
import loggers.logger as log
import files.color as rang

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    cog_name: str = 'Help'
    
    color_list = [
        0xA9FBD7, 0xD7FDEC, 0xFDE74C, 0xE8DAB2, 0xDD6E42, 0xE5FCFF, 0xE5FCFF, 0xABDAFC, 0xACACDE, 0xC490D1, 0xB8336A
    ]
    
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

    @help.command()
    async def blush(self,ctx):
        name='Blush'

        color = await rang.get_color()
        embed = discord.Embed(title='Blush', description='Blush or blush at someone',color=color)
        embed.add_field(name='Syntax', value='`>blush [member]`')
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await self.logger('blush',ctx)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command()
    async def dance(self,ctx):
        name = 'Dance'
        color = await rang.get_color()
        embed = discord.Embed(title='Dance', description='Dance alone or with someone',color=color)
        embed.add_field(name='Syntax', value='`>dance [member]`')
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)
    
    @help.command()
    async def wave(self,ctx):
        name = 'Wave'
        color = await rang.get_color()
        embed = discord.Embed(title='Wave', description='Wave at someone or for any reason',color=color)
        embed.add_field(name='Syntax', value='`>wave [member]`')
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)
    
    @help.command()
    async def sleep(self,ctx):
        name = 'Sleep'
        color = await rang.get_color()
        embed = discord.Embed(title='Sleep', description='Go to sleep',color=color)
        embed.add_field(name='Syntax', value='`>sleep`')
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)
    
    @help.command()
    async def pat(self,ctx):
        name = 'Pat'
        color = await rang.get_color()
        embed = discord.Embed(title='Pat', description='Pats someone',color=color)
        embed.add_field(name='Syntax', value='`>pat [member]`')
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)
    
    @help.command()
    async def cry(self,ctx):
        name = 'Cry'
        color = await rang.get_color()
        embed = discord.Embed(title='Cry', description='Cry at someone or alone',color=color)
        embed.add_field(name='Syntax', value='`>cry [member]`')
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)
    
    @help.command()
    async def pout(self,ctx):
        name = 'Pout'
        color = await rang.get_color()
        embed = discord.Embed(title='Pout', description='Pout at someone or alone',color=color)
        embed.add_field(name='Syntax', value='`>pout [member]`')
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)
    
    @help.command()
    async def kiss(self,ctx):
        name = 'Kiss'
        color = await rang.get_color()
        text = 'Kiss someone..'
        syntax = '`>kiss <member>`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)
    
    @help.command()
    async def bully(self,ctx):
        name = 'Bully'
        color = await rang.get_color()
        text = 'Bully the meanine... or be one.'
        syntax = '`>bully <member>`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)
    
    @help.command()
    async def cuddle(self,ctx):
        name = 'Cuddle'
        color = await rang.get_color()
        text = 'Cuddle with someone. It feels nice.'
        syntax = '`>cuddle <member>`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command()
    async def hug(self,ctx):
        name = 'Hug'
        color = await rang.get_color()
        text = 'Hold someone very close'
        syntax = '`>hold <member>`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)
    
    @help.command()
    async def lick(self,ctx):
        name = 'Lick'
        color = await rang.get_color()
        text = 'Lick something or someone... I don\'t judge my name is literally Coom'
        syntax = '`>lick [member]`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command()
    async def smug(self,ctx):
        name = 'Smug'
        color = await rang.get_color()
        text = 'Act smug'
        syntax = '`>smug [member]`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command()
    async def bonk(self,ctx):
        name = 'Bonk'
        color = await rang.get_color()
        text = 'Bonk em in head'
        syntax = '`>bonk <member>`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command(aliases=['throw'])
    async def yeet(self,ctx):
        name = 'Yeet'
        color = await rang.get_color()
        text = 'Yeet someone tf out.\nAliases: `throw`'
        syntax = '`>yeet <member>`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command(aliases=['happy'])
    async def smile(self,ctx):
        name = 'Smile'
        color = await rang.get_color()
        text = 'Show that you are happy!\naliases: `happy`'
        syntax = '`>smile [member]`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command()
    async def highfive(self,ctx):
        name = 'High five'
        color = await rang.get_color()
        text = 'Give someone a high five!'
        syntax = '`>highfive <member>`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command(aliases=['hold'])
    async def handhold(self,ctx):
        name = 'Hand hold'
        color = await rang.get_color()
        text = 'Hold someone\'s hand. Very cute.\nAliases: `hold`'
        syntax = '`>hold <member>`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command(aliases=['hungry'])
    async def eat(self,ctx):
        name = 'Eat'
        color = await rang.get_color()
        text = 'Eat something alone or with someone.\nAliases: `hungry`'
        syntax = '`>hold [member]`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command(aliases=['nom'])
    async def bite(self,ctx):
        name = 'Bite'
        color = await rang.get_color()
        text = 'Bite someone.\nAliases: `nom`'
        syntax = '`>bite <member>`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command(aliases=['superhug'])
    async def glomp(self,ctx):
        name = 'Glomp'
        color = await rang.get_color()
        text = 'Hold someone very close... with a bit of passion. Just make sure you don\'t hurt yourself.\nAliases: `superhug`'
        syntax = '`>glomp <member>`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command()
    async def slap(self,ctx):
        name = 'Slap'
        color = await rang.get_color()
        text = 'Similar to patting a person.. with a bit more force.'
        syntax = '`>slap <member>`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command()
    async def kill(self,ctx):
        name = 'Kill'
        color = await rang.get_color()
        text = 'Just murder someone I guess idk'
        syntax = '`>kill <member>`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command()
    async def kick(self,ctx):
        name = 'Kick'
        color = await rang.get_color()
        text = 'Similar to slapping but done with legs.'
        syntax = '`>kick <member>`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command()
    async def wink(self,ctx):
        name = 'Wink'
        color = await rang.get_color()
        text = 'Wink ;)'
        syntax = '`>wink [member]`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command()
    async def poke(self,ctx):
        name = 'Poke'
        color = await rang.get_color()
        text = 'Poke someone to act cute... or annoying.'
        syntax = '`>poke <member>`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

    @help.command()
    async def cringe(self,ctx):
        name = 'Cringe'
        color = await rang.get_color()
        text = 'Cringe is what most of will do after reading these descriptions.'
        syntax = '`>cringe <member>`'
        embed = discord.Embed(title=name, description=text,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)


    ########################
    # FUN COG HELP SECTION #
    ########################

    @help.command()
    async def emojify(self,ctx):
        name = 'Emojify'
        color = await rang.get_color()
        text = 'Emojifies the :fire: text by adding emojis :heart_decoration::male_sign: all :joy::persevere: over :sweat_drops::b: it. :drooling_face:\nMaximum 1500 characters. :woman::busts_in_silhouette:'
        embed = discord.Embed(title='Emojify', description=text,color=color)
        embed.add_field(name='Syntax', value='`>emojify <text>`')
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)
    
    @help.command()
    async def owoify(self,ctx):
        name = 'OwOify'
        color = await rang.get_color()
        text = 'Haiiii! OwOifies da text to wook mowe wike fuwwy speak <{^v^}>\nMaximum 1800 chawactews. (❁´◡`❁)'
        embed = discord.Embed(title='OwOify', description=text,color=color)
        embed.add_field(name='Syntax', value='`>OwOify <text>`')
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)
    
    @help.command(aliases=['dadjoke'])
    async def pun(self,ctx):
        name = 'Pun'
        description = 'Sends a random dad joke.\nEach dad joke is assigned with an ID found in footer. Add ID next to command to get joke assigned to ID.\nAlias: `dadjoke`'
        syntax = '`>pun [id]`'
        color = await rang.get_color()
        embed = discord.Embed(title=name,description=description,color=color)
        embed.add_field(name='Syntax', value=syntax)
        embed.set_footer(text='Argument is: <required>, [optional]')
        await ctx.send(embed=embed)
        await log.event_logger(ctx,name,self.cog_name)

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