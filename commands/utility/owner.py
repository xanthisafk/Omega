import discord
from discord.ext import commands
import asyncio
import APIs.color as rang

import codecs
import json


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client
        r = client.config
        self.EMOTE_ERROR = r['emotes']['ERROR']
        self.EMOTE_OK = r['emotes']['OK']
        self.EMOTE_WARNING = r['emotes']['WARNING']
        self.OWNER = r['general']['OWNER']
        self.NAME = r['general']['NAME']
        self.DEBUG = r['debug']['CHANNEL']
        r = None

    @commands.command(name='eval', hidden=True)
    async def eval(self, ctx, *, code):
        """Evaluates code"""
        if not ctx.author.id in self.OWNER:
            return
        result = eval(code)
        await ctx.send(result)

    @eval.error
    async def eval_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            pass
        else:
            await ctx.send(error)
            raise error

    @commands.command(name='exec', hidden=True)
    async def exec(self, ctx, *, code):
        """Executes code"""
        if not ctx.author.id in self.OWNER:
            return
        exec(code)
        await ctx.message.add_reaction(self.EMOTE_OK)

    @exec.error
    async def exec_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            pass
        else:
            await ctx.send(error)
            raise error

    @commands.command()
    async def changeinternalname(self,ctx,*,name):
        if not ctx.author.id in self.OWNER:
            return
        message = await ctx.send(f"{self.EMOTE_WARNING} Bot's internal name will change to **`{name}`** from **`{self.NAME}`**.\nPress {self.EMOTE_OK} to continue.\n*You have 60 seconds to react.*")
        await message.add_reaction(self.EMOTE_OK)
        await message.add_reaction(self.EMOTE_ERROR)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in [self.EMOTE_OK, self.EMOTE_ERROR]

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == self.EMOTE_OK:
                with codecs.open('config.json', 'r', encoding='utf-8') as f:
                    r = json.load(f)

                r['general']['NAME'] = name

                with codecs.open('config.json', 'w', encoding='utf-8') as f:
                    data = json.dumps(r, indent=4)
                    f.write(data)

                with codecs.open('config.json', 'r', encoding='utf-8') as f:
                    r = json.load(f)
                    self.NAME = r['general']['NAME']

                if self.NAME == name:
                    await ctx.send(f"Bot's internal name has been changed to **`{self.NAME}`**.")
                    await message.delete()

            elif str(reaction.emoji) == self.EMOTE_ERROR:
                await message.edit(content="Operation was cancelled.")
                await message.clear_reactions()
                return

            else:
                await ctx.remove_reaction(self.EMOTE_OK, user)

        except asyncio.TimeoutError:
            await message.edit(content=f"Operation was cancelled because message timed out.")
            await message.clear_reactions()
            return

    @changeinternalname.error
    async def changeinternalname_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(("Error: You are missing an argument"))
        else:
            await ctx.send(error)
            raise error

    @commands.command()
    async def addowner(self,ctx,member:discord.Member):
        if not ctx.author.id in self.OWNER:
            return

        if member.id in self.OWNER:
            return await ctx.send(f"{member.mention} is already an owner.")

        message = await ctx.send(f"{member.mention} will be added to the list of bot owners.\nPress {self.EMOTE_OK} to continue.\n*You have 60 seconds to react.*")
        await message.add_reaction(self.EMOTE_OK)
        await message.add_reaction(self.EMOTE_ERROR)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in [self.EMOTE_OK, self.EMOTE_ERROR]

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == self.EMOTE_OK:
                with codecs.open('config.json', 'r', encoding='utf-8') as f:
                    r = json.load(f)

                r['general']['OWNER'].append(member.id)

                with codecs.open('config.json', 'w', encoding='utf-8') as f:
                    data = json.dumps(r, indent=4)
                    f.write(data)

                with codecs.open('config.json', 'r', encoding='utf-8') as f:
                    r = json.load(f)
                    self.OWNER = r['general']['OWNER']

                if member.id in self.OWNER:
                    await message.delete()
                    await ctx.send(f"{self.EMOTE_OK} {member.mention} has been added to the list of bot owners.")

            elif str(reaction.emoji) == self.EMOTE_ERROR:
                await message.edit(content="Operation was cancelled.")
                await message.clear_reactions()
                return

            else:
                await ctx.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            await message.edit(content=f"Operation was cancelled because message timed out.")
            await message.clear_reactions()
            return

    @addowner.error
    async def addowner_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, commands.BadArgument):
            await ctx.send(("Error: "+error))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(("Error: You are missing an argument"))
        else:
            await ctx.send(error)
            raise error

    @commands.command()
    async def removeowner(self,ctx,member:discord.Member):
        if not ctx.author.id in self.OWNER:
            return
        if member.id not in self.OWNER:
            return await ctx.send(f"{member.mention} is not an owner.")

        if len(self.OWNER) == 1:
            return await ctx.send(f"<@{self.OWNER[0]}> is the only owner and you cannot remove them.")

        message = await ctx.send(f"{self.EMOTE_WARNING} will be removed as the bot's owner.\nPress {self.EMOTE_OK} to continue.\n*You have 60 seconds.*")
        await message.add_reaction(self.EMOTE_OK)
        await message.add_reaction(self.EMOTE_ERROR)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in [self.EMOTE_OK, self.EMOTE_ERROR]

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == self.EMOTE_OK:
                with codecs.open('config.json', 'r', encoding='utf-8') as f:
                    r = json.load(f)

                r['general']['OWNER'].remove(member.id)

                with codecs.open('config.json', 'w', encoding='utf-8') as f:
                    data = json.dumps(r, indent=4)
                    f.write(data)

                with codecs.open('config.json', 'r', encoding='utf-8') as f:
                    r = json.load(f)
                    self.OWNER = r['general']['OWNER']

                if member.id not in self.OWNER:
                    await message.delete()
                    await ctx.send(f"{self.EMOTE_OK} {member.mention} has been removed from the list of bot owners.")

            elif str(reaction.emoji) == self.EMOTE_ERROR:
                await message.edit(content="Operation was cancelled.")
                await message.clear_reactions()
                return

            else:
                await ctx.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            await message.edit(content=f"Operation was cancelled because message timed out.")
            await message.clear_reactions()
            return

    @removeowner.error
    async def removeowner_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, commands.BadArgument):
            await ctx.send(("Error: "+error))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(("Error: You are missing an argument"))
        else:
            await ctx.send(error)
            raise error

    @commands.command()
    async def changedebugchannel(self,ctx,new:discord.TextChannel):

        if not ctx.author.id in self.OWNER:
            return

        old = self.client.get_channel(self.DEBUG)
        message = await ctx.send(f"{self.EMOTE_WARNING} This operation will change debug channel from **{old.mention}** to **{new.mention}**.\nPress {self.EMOTE_OK} to continute.\n*You have 60 seconds to respond or the operation is automatically cancelled.*")
        await message.add_reaction(self.EMOTE_OK)
        await message.add_reaction(self.EMOTE_ERROR)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in [self.EMOTE_OK, self.EMOTE_ERROR]

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == self.EMOTE_OK:
                with codecs.open('config.json', 'r', encoding='utf-8') as f:
                    r = json.load(f)

                r['debug']['CHANNEL'] = new.id

                with codecs.open('config.json', 'w', encoding='utf-8') as f:
                    data = json.dumps(r, indent=4)
                    f.write(data)

                with codecs.open('config.json', 'r', encoding='utf-8') as f:
                    r = json.load(f)
                    self.DEBUG = r['debug']['CHANNEL']

                self.client.config['debug']['CHANNEL'] = self.DEBUG

                await message.delete()
                await ctx.send(f"{self.EMOTE_OK} Debug channel has been changed from **{old.mention}** to **{new.mention}**.")

            elif str(reaction.emoji) == self.EMOTE_ERROR:
                await message.edit(content="Operation was cancelled.")
                await message.clear_reactions()
                return

            else:
                await ctx.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            await message.edit(content=f"Operation was cancelled because message timed out.")
            await message.clear_reactions()
            return

    @changedebugchannel.error
    async def changedebugchannel_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, commands.BadArgument):
            await ctx.send(("Error: "+error))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(("Error: You are missing an argument"))
        else:
            await ctx.send(error)
            raise error

    @commands.command()
    async def addprefix(self,ctx,new:str):
        if not ctx.author.id in self.OWNER:
            return

        if new in self.client.config['general']['PREFIX']:
            return await ctx.send(f"{self.EMOTE_ERROR} The new prefix is already in use.")

        message = await ctx.send(f"{self.EMOTE_WARNING} This operation will add **`{new}`** to bot's prefixes.\nPress {self.EMOTE_OK} to continute.\n*You have 60 seconds to respond or the operation is automatically cancelled.*")

        await message.add_reaction(self.EMOTE_OK)
        await message.add_reaction(self.EMOTE_ERROR)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in [self.EMOTE_OK, self.EMOTE_ERROR]

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == self.EMOTE_OK:
                with codecs.open('config.json', 'r', encoding='utf-8') as f:
                    r = json.load(f)

                r['general']['PREFIX'].append(new)

                with codecs.open('config.json', 'w', encoding='utf-8') as f:
                    data = json.dumps(r, indent=4)
                    f.write(data)

                with codecs.open('config.json', 'r', encoding='utf-8') as f:
                    r = json.load(f)
                    self.client.config['general']['PREFIX'] = r['general']['PREFIX']

                await message.delete()
                await ctx.send(f"{self.EMOTE_OK} The bot's prefix has been updated.\nCurrent prefixes: `{', '.join(self.client.config['general']['PREFIX'])}`\nYou may need to restart the bot to see the effect.")

            elif str(reaction.emoji) == self.EMOTE_ERROR:
                await message.clear_reactions()
                await message.edit(content=f"{self.EMOTE_WARNING} Operation was cancelled.")
                return

            else:
                await ctx.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            await message.edit(content=f"{self.EMOTE_WARNING} Operation was cancelled because message timed out.")
            await message.clear_reactions()
            return

    @addprefix.error
    async def addprefix_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, commands.BadArgument):
            await ctx.send(("Error: "+error))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(("Error: You are missing an argument"))
        else:
            await ctx.send(error)
            raise error

    @commands.command()
    async def removeprefix(self,ctx,new:str):
        if not ctx.author.id in self.OWNER:
            return

        if new not in self.client.config['general']['PREFIX']:
            return await ctx.send(f"{self.EMOTE_ERROR} The prefix is not in use.")

        if len(self.client.config['general']['PREFIX']) == 1:
            return await ctx.send(f"{self.EMOTE_ERROR} You can't remove the only prefix.")

        message = await ctx.send(f"{self.EMOTE_WARNING} This operation will remove **`{new}`** from bot's prefixes.\nPress {self.EMOTE_OK} to continute.\n*You have 60 seconds to respond or the operation is automatically cancelled.*")

        await message.add_reaction(self.EMOTE_OK)
        await message.add_reaction(self.EMOTE_ERROR)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in [self.EMOTE_OK, self.EMOTE_ERROR]

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == self.EMOTE_OK:
                with codecs.open('config.json', 'r', encoding='utf-8') as f:
                    r = json.load(f)

                r['general']['PREFIX'].remove(new)

                with codecs.open('config.json', 'w', encoding='utf-8') as f:
                    data = json.dumps(r, indent=4)
                    f.write(data)

                with codecs.open('config.json', 'r', encoding='utf-8') as f:
                    r = json.load(f)
                    self.client.config['general']['PREFIX'] = r['general']['PREFIX']

                await message.delete()
                await ctx.send(f"{self.EMOTE_OK} The bot's prefix has been updated.\nCurrent prefixes: `{', '.join(self.client.config['general']['PREFIX'])}`\nYou may need to restart the bot to see the effect.")

            elif str(reaction.emoji) == self.EMOTE_ERROR:
                await message.clear_reactions()
                await message.edit(content=f"{self.EMOTE_WARNING} Operation was cancelled.")
                return

            else:
                await ctx.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            await message.edit(content=f"{self.EMOTE_WARNING} Operation was cancelled because message timed out.")
            await message.clear_reactions()
            return

    @removeprefix.error
    async def removeprefix_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, commands.BadArgument):
            await ctx.send(("Error: "+error))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(("Error: You are missing an argument"))
        else:
            await ctx.send(error)
            raise error

    @commands.command()
    async def listemote(self,ctx):

        if not ctx.author.id in self.OWNER:
            return


        embed = discord.Embed(title="Admin panel", description="Current emojis...", color=discord.Color.random())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        for emote in self.client.config['emotes']:
            embed.add_field(name=emote, value=self.client.config['emotes'][emote])

        embed.set_footer(text=f'Use {self.client.config["general"]["PREFIX"][0]}updateemote <emotename> <updatedemote>')

        await ctx.send(embed=embed)

    @listemote.error
    async def listemote_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(("Error: You are missing an argument"))
        else:
            await ctx.send(error)
            raise error

    @commands.command()
    async def updateemote(self,ctx,emote:str,new):
        if ctx.author.id not in self.OWNER:
            return

        if emote.upper() not in self.client.config['emotes']:
            return await ctx.send(f"{self.EMOTE_ERROR} The emote is not in use.")

        message = await ctx.send(f"{self.EMOTE_WARNING} Emote {self.client.config['emotes'][emote.upper()]} will be replaced by {new}.\nPress{self.EMOTE_OK} to confirm.\n*You have 60 seconds to respond.*")

        await message.add_reaction(self.EMOTE_OK)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == self.EMOTE_OK

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == self.EMOTE_OK:
                with codecs.open('config.json', 'r', encoding='utf-8') as f:
                    r = json.load(f)

                r['emotes'][emote.upper()] = str(new)

                with codecs.open('config.json', 'w', encoding='utf-8') as f:
                    data = json.dumps(r, indent=4)
                    f.write(data)

                with codecs.open('config.json', 'r', encoding='utf-8') as f:
                    r = json.load(f)
                    self.client.config['emotes'] = r['emotes']

                embed = discord.Embed(title="Admin panel", description="Current emojis...", color=discord.Color.random())
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

                for emote in self.client.config['emotes']:
                    embed.add_field(name=emote, value=self.client.config['emotes'][emote])

                await message.clear_reactions()
                await message.edit(content=f"{self.EMOTE_OK} The emote has been updated.",embed=embed)

            else:
                await message.clear_reactions()
                await message.edit(content=f"{self.EMOTE_WARNING} Operation was cancelled.")
                return

        except asyncio.TimeoutError:
            await message.edit(content=f"{self.EMOTE_WARNING} Operation was cancelled because message timed out.")
            await message.clear_reactions()
            return

    @updateemote.error
    async def updateEmote_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, commands.BadArgument):
            await ctx.send(("Error: "+error))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(("Error: You are missing an argument"))
        else:
            await ctx.send(error)
            raise error






def setup(client):
    client.add_cog(Owner(client))