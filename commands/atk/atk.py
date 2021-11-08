import random
import re
from datetime import datetime

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
        self.dt = {}
        self.keys  = []

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

        for i in range(length):
            if range(length) == 0:
                self.atks={}
                return self.atks
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

        length = len(ignores)
        if length == 0:
            return self.aignores

        for i in range(length):
            self.aignores.append(ignores[i][0])
        return self.aignores

    @commands.command(aliases=["atk_ignore"])
    async def ignore(self, ctx: commands.Context, user = None) -> None:
        """
        Adds the user to a list of ignored users. People who use this function no longer trigger ATKs.

        args:
            ctx: commands.Context -> ctx given by discord library
        returns:
            None (Adds user to database)
        """
        command_name = "Ignore"
        if user is None or not isinstance(user, discord.Member):
            id = str(ctx.author.id)
        else:
            if ctx.author.has_permissions(administrator=True):
                id = str(user.id) + "--admin"
            else:
                raise commands.MissingRole()

        data = self.aignores

        if id in data:
            await ctx.reply(f'{config.EMOTE_ERROR} Error: You are already on list.')
            return

        await self.p.insert(table='ignores', fields='id', values=id)
        await self.p.commit()
        await self.get_new_ignores()
        await ctx.reply(f"{config.EMOTE_OK} Success: You are added to list")
    
    @ignore.error
    async def ignore_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(f'{config.EMOTE_ERROR} Error: You do not have permission to use this command.')
        else:
            await ctx.reply(f"{config.EMOTE_ERROR} Something unexpected happened.")
            raise error

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

        except Exception as e:
            await ctx.reply("Something went wrong")
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

        except Exception as e:

            await ctx.send(f"{config.EMOTE_ERROR}: Something went wrong.")
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
            message: discord.Message -> The message
        returns:
            None
        """

        # If messege sender is the bot, ignore
        if message.author == self.client.user or message.author.bot:
            return
        try:
            # If message sender is in ignore list, ignore
            if str(message.author.id) in self.aignores:
                return
        except Exception:
            pass

        # Check for timestamp
        def check():
            try:
                last = self.dt[message.guild.id][message.author.id]
            except: return True

            if (datetime.utcnow() - last).total_seconds() < 5:
                for x in message.mentions:
                    if(x == self.client.user):
                        return False
                return False
            else:
                return True

        # Check for URL
        def urlcheck():
            if re.search(r'(https?://\S+)', message.content): return False
            else: return True

        # Check if message starts with special characters
        spechar = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', '|', '\\', ':', '"', '<', '>', '?', '/', '`', '~', '.', ',']
        def specialcheck():
            if any (x in message.content for x in spechar): return False
            else: return True

        # Lower case message
        s = message.content.lower()

        # Split message into words
        split_s = s.split(' ')

        # if sentence starts with a special characters, ignore
        for i in spechar:
            if s.startswith(i):
                return

        # if sentence starts with prefix, ignore
        if any (x in s for x in config.PREFIX):
            return

        # If message starts with prefix
        for word in split_s:
            for i in config.PREFIX:
                if word.startswith(i):
                    return

            if re.search(r'\bnooooo', word):
                if check():
                    await message.channel.send(random.choice(self.atks['nooooo']))
                else:
                    return await message.add_reaction(random.choice(['⌚','⏳','⏰','🕛','🕐','🕖','🕕','🕔','🕚','🕙','🕓','🕒','🕗','🕑']))
                return self.dt.update({message.guild.id: {message.author.id: datetime.utcnow()}})

            if re.search(r'\bhhh', word):
                if check():
                    await message.channel.send(self.atks['hhh'])
                else:
                    return await message.add_reaction(random.choice(['⌚','⏳','⏰','🕛','🕐','🕖','🕕','🕔','🕚','🕙','🕓','🕒','🕗','🕑']))
                return self.dt.update({message.guild.id: {message.author.id: datetime.utcnow()}})

        potential_atk = []
        for i in self.keys:
            if i in s:
                potential_atk.append(i)

        if len(potential_atk) <= 0:
            return
        
        potential_atk.sort(key=len, reverse=True)
        
        for i in potential_atk:
            regex = re.compile(rf'\b{i}\b')
            if regex.search(s):
                if check():
                    if type(self.atks[i]) == list:
                        await message.channel.send(random.choice(self.atks[i]))
                    else:
                        await message.channel.send(self.atks[i])
                else:
                    return await message.add_reaction(random.choice(['⌚','⏳','⏰','🕛','🕐','🕖','🕕','🕔','🕚','🕙','🕓','🕒','🕗','🕑']))
                return self.dt.update({message.guild.id: {message.author.id: datetime.utcnow()}})

        for x in message.mentions:
            if(x == self.client.user):
                if random.randrange(1, 10) == 7:
                    await message.channel.send('Sorry, I\'m busy right now:')
                    await message.channel.send('https://media.discordapp.net/attachments/845191720224161824/889751939053682748/coom.png')

                else:
                    return

    @commands.command(name='flush', aliases=['flush_atks','reload_atk','reload_atks','flush_irgnore','flush_ignores'])
    @commands.is_owner()
    async def flush_atks(self, ctx) -> None:
        await self.get_new_atks()
        await self.get_new_ignores()
        await ctx.message.add_reaction(config.EMOTE_OK)

    @commands.command(name='atk_list', aliases=['atk_list_all','atk_list_all_atks','list_atk','listatk'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def atk_list(self, ctx) -> None:
        cog = self.client.get_cog('Help')
        await ctx.invoke(cog.atk_help)

    @flush_atks.error
    async def flush_atks_error(self, ctx, error):
        await ctx.message.add_reaction(config.EMOTE_ERROR)
        raise error

    @atk_list.error
    async def atk_list_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'{config.EMOTE_ERROR} You are on cooldown for next {error.retry_after}')
        else:
            await ctx.reply("Some unexpected error occured")
            raise error



def setup(client):
    client.add_cog(ATK(client))
