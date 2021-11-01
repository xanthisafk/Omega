import random
import re

import APIs.db as pql
import config
import discord
import loggers.logger as log
from discord.ext import commands


class ATK(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[9:].capitalize()
        self.p = pql.PostgreSQL(DB_HOST=config.DB_HOST, DB_USER=config.DB_USER,
                                DB_PASS=config.DB_PASS, DB_NAME=config.DB_NAME)
        self.tempp = 0
        self.atks = {}

    @commands.Cog.listener()
    async def on_ready(self):
        atkS = "CREATE TABLE IF NOT EXISTS atks(name VARCHAR(255) PRIMARY KEY, value VARCHAR(255) NOT NULL)"
        ignS = "CREATE TABLE IF NOT EXISTS ignores(id VARCHAR(255) PRIMARY KEY NOT NULL)"
        await self.p.execute(atkS)
        await self.p.execute(ignS)
        try:
            await self.p.commit()
        except:
            pass
        if not self.tempp == 0:
            await self.p.connect(DB_HOST=config.DB_HOST, DB_USER=config.DB_USER, DB_PASS=config.DB_PASS, DB_NAME=config.DB_NAME)
        self.tempp += 1

        self.atks = await self.get_new_atks()
        self.aignores = await self.get_new_ignores()

    # get new atks list

    async def get_new_atks(self) -> list:
        
        """
        Function that retrives a new list of updated ATK list and assigns it to global variable

        agrs:
            None
        returns:
            self.aatk: list -> List of all available ATKs currently registered
        """

        # Get keys
        string = "SELECT name FROM atks"
        atk = await self.p.execute(string)

        self.keys = []
        length = len(atk)

        for i in range(0, length):
            self.keys.append(atk[i][0])

        string = "SELECT value FROM atks"

        # Get values
        values = await self.p.execute(string)

        self.value = []
        length = len(values)

        for i in range(0, length):
            self.value.append(values[i][0])

        # Zip together and create dictionary
        self.atks = dict(zip(self.keys, self.value))

        # list things.
        for name in self.atks:
            if '&&' in self.atks[name]:
                l = self.atks[name].split('&&')
                self.atks[name] = l

        # return
        return self.atks

    # get new ignores list
    async def get_new_ignores(self) -> list:
        """
    Function that retrives a new list of updated ignored list and assigns it to global variable.

    agrs:
        None
    returns:
        self.aignores: list -> List of all available ATKs currently registered
    """
        string = "SELECT id FROM ignores"
        ignores = await self.p.execute(string)

        self.aignores = []

        length = len(ignores)-1
        if length == 0:
            length += 1

        for i in range(0, length):
            self.aignores.append(ignores[i][0])

        return self.aignores

    @commands.command(aliases=["atk_ignore"])
    async def ignore(self, ctx: commands.Context) -> None:
        """
        Adds the user to a list of ignored users. People who use this function no longer trigger ATKs.

        args:
            ctx: commands.Context -> ctx given by discord library
        returns:
            None (Adds user to database)
        """
        command_name = "Ignore"
        try:
            id = str(ctx.author.id)

            data = self.aignores

            if id in data:
                await ctx.reply(f'{config.EMOTE_ERROR} Error: You are already on list.')
                return

            await self.p.insert(table='ignores', fields='id', values=id)
            await self.p.commit()
            await self.get_new_ignores()
            await ctx.reply(f"{config.EMOTE_OK} Success: You are added to list")
            await log.logger(ctx,command_name,self.cog_name,'INFO')

        except Exception as e:
            await ctx.reply("Something went wrong")
            await log.logger(ctx,command_name,self.cog_name,'ERROR', e)
            raise e

    @commands.command(aliases=["atk_unignore"])
    async def unignore(self, ctx: commands.Context) -> None:
        """
        Removes id of user from list of ignored people.

        args:
            ctx: commands.Context -> ctx given by discord library
        :returns
            None (removes user from database)
        """
        command_name = 'Unignore'
        try:
            id = str(ctx.author.id)

            if id not in self.aignores:
                await ctx.reply(f"{config.EMOTE_ERROR} Error: You are not in ignore list.")
                return

            string = f"DELETE FROM ignores WHERE id = '{id}'"
            await self.p.execute(string)
            await self.p.commit()
            await self.get_new_ignores()
            await ctx.reply(f"{config.EMOTE_OK} Success: You are removed from ignore list.")
            await log.logger(ctx,command_name,self.cog_name,'INFO')

        except Exception as e:
            await ctx.reply("Something went wrong")
            await log.logger(ctx,command_name,self.cog_name,'ERROR', e)
            raise e

    @commands.command(aliases=["atk_add"])
    @commands.has_permissions(administrator=True)
    async def add_atk(self, ctx: commands.Context, *, string: str) -> None:
        """
        Creates a new keyword for auto trigger keywords.

        args:
            ctx: commands.Context -> instance of Disocrd context
            string: str -> name and value of ATK; seperated by a comma. (name,value)(value must be less than 255 characters.)
        returns:
            None
        """
        command_name = 'Add_ATK'
        try:

            x = string.split(",", 1)
            try:
                name = x[0].rstrip()
                url = x[1]
                if len(url) > 255:
                    await ctx.send(f"{config.EMOTE_ERROR} Value must be under 255 characters.")
                    return

            except Exception as e:
                if isinstance(e, IndexError):
                    await ctx.send("Please enter in format of `text1, text2` (Comma is important)")
                    return

            name = name.lower()

            if name in self.atks:
                await ctx.send(f"{config.EMOTE_ERROR} Error: `{name}` already bound")
                return

            string = f"INSERT INTO atks(name,value) VALUES('{name}','{url}')"
            await self.p.execute(string)
            await self.p.commit()
            await self.get_new_atks()

            if name in self.atks:
                await ctx.send(f'{config.EMOTE_OK} Success: `{name}` is now bound.')

            else:
                e = f'{config.EMOTE_ERROR} Error: `{name}` could not be bound'
                await ctx.send(e)
                await log.logger(ctx,command_name,self.cog_name,'ERROR',e)

        except Exception as e:

            await ctx.send(f"{config.EMOTE_ERROR}: Something went wrong.")
            await log.logger(ctx,command_name,self.cog_name,'ERROR',e)
            raise e

    @commands.command(aliases=["atk_remove", "atk_delete"])
    @commands.has_permissions(administrator=True)
    async def remove_atk(self, ctx, *, name: str,) -> None:
        command_name = 'Remove_ATK'
        try:

            name = name.lower()
            if name in self.atks:
                string = f"DELETE FROM atks WHERE name='{name}'"
            else:
                await ctx.send(f'{config.EMOTE_ERROR} Error: `{name}` not found.')
                return

            await self.p.execute(string)
            await self.p.commit()
            await self.get_new_atks()

            if name not in self.atks:
                await ctx.send(f"{config.EMOTE_OK} Success: `{name}` is removed")
                await log.logger(ctx,command_name,self.cog_name,'INFO')

            else:
                e = f'Error: `{name}` could not be bound'
                await ctx.send(e.capitalize())
                await log.logger(ctx,name,self.cog_name,'ERROR',e)

        except Exception as e:
            await ctx.send(f"{config.EMOTE_ERROR}: Something went wrong")
            await log.logger(ctx,name,self.cog_name,'ERROR',e)
            raise e

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        """
        This function processes the message to check if they contain an ATK. If it does, then send the assigned
        value back.

        args:
            message: discord.Context -> Contains all the information needed to process the message
        returns:
            None
        """

        if message.author == self.client.user or message.author.bot:
            return
        try:
            if str(message.author.id) in self.aignores:
                return
        except Exception:
            pass

        s = message.content.lower()

        split_s = s.split(' ')

        if s.startswith('>'):
            return

        for word in split_s:

            if word.startswith(':') or word.startswith('>') or word.startswith('-'):
                return

            if re.search(r'\bnooooo', word):

                await message.channel.send(random.choice(self.atks['nooooo']))
                await log.logger(message,s,self.cog_name,'INFO')
                return
            
            if re.search(r'\bhhh', word):

                await message.channel.send(self.atks['hhh'])
                await log.logger(message,s,self.cog_name,'INFO')

        try:
            for word in self.atks:

                check1 = r":"+word+r":"
                check2 = r"\b-"+word+r"\b"
                check3 = r"\b>"+word+r"\b"
                if re.search(check1, s) or re.search(check2, s) or re.search(check3, s):
                    return

                regex_string = r"\b"+word + r"\b"

                if re.search(regex_string, s):

                    if type(self.atks[word]) == list:
                        await message.channel.send(random.choice(self.atks[word]))
                        await log.logger(message,s,self.cog_name,'INFO')
                        return

                    else:
                        await message.channel.send(self.atks[word])
                        await log.logger(message,s,self.cog_name,'INFO')
                        return

        except Exception as e:

            if isinstance(e, IndexError):
                await message.channel.send("Please enter in format of `text1, text2` (Comma is important)")
            else:
                await message.channel.send('Something went wrong.')
                await log.logger(message,s,self.cog_name,'ERROR',e)
                raise e

        for x in message.mentions:
            if(x == self.client.user):
                if random.randrange(1, 10) == 7:
                    await message.channel.send('Sorry, I\'m busy right now:')
                    await message.channel.send('https://media.discordapp.net/attachments/845191720224161824/889751939053682748/coom.png')

                    s = 'Mentioned'
                    await log.logger(message,s,self.cog_name,'INFO')
                else:
                    return



def setup(client):
    client.add_cog(ATK(client))
