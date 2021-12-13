import random
import re
from datetime import datetime
import codecs
import json

import discord
import loggers.logger as log
from discord.ext import commands
import redis


class ATK(commands.Cog):
    def __init__(self, client):
        self.client = client
        with codecs.open('config.json', 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        data = self.config['redis']
        self.redis = redis.StrictRedis(host=data['HOST'], port=data['PORT'], password=data['PASS'])
        self.tempp = 0
        self.atks = {}
        self.dt = {}
        self.keys  = []

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.tempp == 0:
            data = self.config['redis']
            self.redis = redis.StrictRedis(host=data['HOST'], port=data['PORT'], password=data['PASS'])
        self.tempp == 1

        self.atks = await self.get_new_atks()
        self.aignores = await self.get_new_ignores()


    ##############################
    #  Database Update Commands  #
    ##############################

    # Update the database with the new atks
    async def set_new_atks(self,data) -> dict:

        return self.redis.execute_command("JSON.SET", "atks", ".", json.dumps(data))

    # Retrieve the atks from the database
    async def get_new_atks(self) -> dict:

        self.atks = json.loads(self.redis.execute_command("JSON.GET", "atks"))
        return self.atks

    # Update the database with the new ignores
    async def set_new_ignores(self,data) -> dict:

            return self.redis.execute_command("JSON.SET", "ignores", ".", json.dumps(data))

    # Retrieve the database with the new ignores
    async def get_new_ignores(self) -> dict:

        self.aignores = json.loads(self.redis.execute_command("JSON.GET", "ignores"))
        return self.aignores

    ##############################
    #      Command Functions     #
    ##############################

    @commands.command(aliases=["atk_ignore"])
    async def ignore(self, ctx: commands.Context, user:discord.Member = None, *, args='') -> None:

        willBeLocked = False
        if not isinstance(user, discord.Member):
            id = str(ctx.author.id)
        else:
            if ctx.author.guild_permissions.administrator:
                id = str(user.id)
                if 'lock' in args:
                    id = id + 'lock'
                    willBeLocked = True
            else:
                return await ctx.send(f"{self.config['emotes']['ERROR']} Error: You do not have permission to do that.")

        guild = str(ctx.guild.id)
        try:
            
            data = self.aignores[guild]
        except KeyError:
            self.aignores.update({guild: []})
            data = self.aignores[guild]

        if id in data or id+"lock" in data:
            await ctx.reply(f'{self.config["emotes"]["ERROR"]} Error: {user.mention if(user) else ctx.author.mention} is already on list.')
            return

        data.append(id)
        self.aignores[guild] = data
        await self.set_new_ignores(self.aignores)
        await self.get_new_ignores()

        await ctx.reply(f"{self.config['emotes']['OK']} Success: {user.mention if(user) else ctx.author.mention} will be ignored{' and has been locked from using ATKs.' if willBeLocked else '.'}")

    @ignore.error
    async def ignore_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(f'{self.config["emotes"]["ERROR"]} Error: You do not have permission to use this command.')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply(f"{self.config['emotes']['ERROR']} Error: User `{error.argument}` not found.")
        else:
            await ctx.reply(f"{self.config['emotes']['ERROR']} Something unexpected happened.")
            raise error

    @commands.command(aliases=["atk_unignore"])
    async def unignore(self, ctx: commands.Context, user:discord.Member = None) -> None:

        if user is None:
            id = str(ctx.author.id)
        else:
            id = str(user.id)

        guild = str(ctx.guild.id)
        try:
            data = self.aignores[guild]
        except KeyError:
            self.aignores.update({guild: []})
            data = self.aignores[guild]

        lock = id+"lock"

        if id not in data and lock not in data:
            return await ctx.reply(f"{self.config['emotes']['ERROR']} Error: {user.mention if(user) else ctx.author.mention} is not being ingored.")

        if user != None:
            if str(user.id) in data or str(user.id)+"lock" in data:
                if not ctx.author.guild_permissions.administrator:
                    return await ctx.reply(f"{self.config['emotes']['ERROR']} Error: You do not have permission to use this command.")

        if lock in data:
            if not ctx.author.guild_permissions.administrator:
                return await ctx.reply(f"{self.config['emotes']['ERROR']} Error: An admin has locked you out. Please contact admin to run this command on you.")

        try:
            data.remove(id)
        except ValueError:
            data.remove(lock)

        self.aignores[guild] = data
        await self.set_new_ignores(self.aignores)
        await self.get_new_ignores()

        await ctx.reply(f"{self.config['emotes']['OK']} Success: {user.mention if(user) else ctx.author.mention} is no longer being ignored.")

    @unignore.error
    async def unignore_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(f'{self.config["emotes"]["ERROR"]} Error: You do not have permission to use this command.')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply(f"{self.config['emotes']['ERROR']} Error: User `{error.argument}` not found.")
        else:
            await ctx.reply(f"{self.config['emotes']['ERROR']} Something unexpected happened.")
            raise error


    @commands.command(aliases=["atk_add", 'addatk', 'atkadd', 'addtrigger'])
    @commands.has_permissions(administrator=True)
    async def add_atk(self, ctx: commands.Context, *, string: str) -> None:

        x = string.split(",", 1)
        try:
            name = x[0].rstrip()
            url = x[1].lstrip()
            if len(url) > 1500:
                return await ctx.send(f"{self.config['emotes']['ERROR']} Value must be under **`1500`** characters.")
            if name == '':
                return await ctx.send(f"{self.config['emotes']['ERROR']} Name can not be empty.")

            url = url.split("&&")
            if len(url) == 1:
                url = url[0]

        except Exception as e:
            if isinstance(e, IndexError):
                return await ctx.send("Please enter in format of `text1, text2` (Comma is important)")

        name = name.lower()

        try:
            data = self.atks[str(ctx.guild.id)]
        except KeyError:
            self.atks.update({str(ctx.guild.id): {}})
            data = self.atks[str(ctx.guild.id)]

        if name in data:
            return await ctx.send(f"{self.config['emotes']['ERROR']} Error: **`{name}`** is already bound")

        data.update({name: url})
        self.atks[str(ctx.guild.id)] = data

        await self.set_new_atks(self.atks)
        await self.get_new_atks()

        if name in self.atks[str(ctx.guild.id)]:
            await ctx.send(f'{self.config["emotes"]["OK"]} Success: `{name}` is now bound.')

        else:
            e = f'{self.config["emotes"]["ERROR"]} Error: `{name}` could not be bound'
            await ctx.send(e)

    @add_atk.error
    async def add_atk_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(f'{self.config["emotes"]["ERROR"]} Error: You do not have permission to use this command.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"{self.config['emotes']['ERROR']} Error: Please enter in format of `text1, text2` (Comma is important)")
        else:
            await ctx.reply(f"{self.config['emotes']['ERROR']} Something unexpected happened.")
            raise error

    @commands.command(aliases=["atk_remove", "atk_delete", 'removeatk', 'atkremove', 'removetrigger', 'deletetrigger'])
    @commands.has_permissions(administrator=True)
    async def remove_atk(self, ctx, *, name: str,) -> None:

        name = name.lower()
        
        try:
            data = self.atks[str(ctx.guild.id)]
        except KeyError:
            self.atks.update({str(ctx.guild.id): {}})
            data = self.atks[str(ctx.guild.id)]

        if name in data:
            del data[name]
        else:
            await ctx.send(f'{self.config["emotes"]["ERROR"]} Error: `{name}` not found.')
            return
        
        self.atks[str(ctx.guild.id)] = data
        await self.set_new_atks(self.atks)
        await self.get_new_atks()

        if name not in self.atks[str(ctx.guild.id)]:
            await ctx.send(f"{self.config['emotes']['OK']} Success: `{name}` is removed")


    @remove_atk.error
    async def remove_atk_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply(f'{self.config["emotes"]["ERROR"]} Error: You do not have permission to use this command.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"{self.config['emotes']['ERROR']} Error: Enter `name` of atk that you want to remove.")
        else:
            await ctx.reply(f"{self.config['emotes']['ERROR']} Something unexpected happened.")
            raise error

    @commands.Cog.listener()
    async def on_message(self, message) -> None:

        for x in message.mentions:
            if(x == self.client.user):
                if random.randrange(1, 100) == 7:
                    return await message.reply('Sorry, I\'m busy right now:\nhttps://media.discordapp.net/attachments/845191720224161824/889751939053682748/coom.png')

        # If messege sender is the bot, ignore
        if message.author == self.client.user or message.author.bot:
            return
        try:
            # If message sender is in ignore list, ignore
            if str(message.author.id) in self.aignores[str(message.guild.id)] or (str(message.author.id)+"lock") in self.aignores[str(message.guild.id)]:
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
            if re.search(r'((ftp|http|https):\/\/)?(www.)?(?!.*(ftp|http|https|www.))[a-zA-Z0-9_-]+(\.[a-zA-Z]+)+((\/)[\w#]+)*(\/\w+\?[a-zA-Z0-9_]+=\w+(&[a-zA-Z0-9_]+=\w+)*)?', message.content):
                return True
            else:
                return False


        # Check if message starts with special characters
        spechar = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', '|', '\\', ':', '"', '<', '>', '?', '/', '`', '~', '.', ',']
        def specialcheck():
            for x in spechar:
                if message.content.startswith(x):
                    
                    if re.search(r"<[?@!:]+[0-9]+>", message.content):
                        pass
                    else:
                        return False
            return True


        # Lower case message
        s = message.content.lower()

        # Split message into words
        split_s = s.split(' ')

        # if sentence starts with a special characters, ignore
        if not specialcheck() or urlcheck():
            return
        


        guild = str(message.guild.id)
        try:
            data = self.atks[guild]
        except KeyError:
            self.atks.update({guild: {}})
            data = self.atks[guild]


        # If message starts with prefix
        for word in split_s:
            for i in self.config['general']['PREFIX']:
                if word.startswith(i):
                    return



            if re.search(r'\bnooooo\b', word):
                if check():
                    await message.channel.send(random.choice(data['nooooo']))
                else:
                    return await message.add_reaction(random.choice(['⌚','⏳','⏰','🕛','🕐','🕖','🕕','🕔','🕚','🕙','🕓','🕒','🕗','🕑']))
                return self.dt.update({message.guild.id: {message.author.id: datetime.utcnow()}})

            if re.search(r'\bhhh', word):
                if check():
                    await message.channel.send(data['hhh'])
                else:
                    return await message.add_reaction(random.choice(['⌚','⏳','⏰','🕛','🕐','🕖','🕕','🕔','🕚','🕙','🕓','🕒','🕗','🕑']))
                return self.dt.update({message.guild.id: {message.author.id: datetime.utcnow()}})


        potential_atk = []
        for i in data:
            if i in s:
                potential_atk.append(i)


        if len(potential_atk) <= 0:
            return

        
        potential_atk.sort(key=len, reverse=True)
        
        for i in potential_atk:
            regex = re.compile(rf'\b{i}\b')
            if regex.search(s):
                if check():
                    if type(data[i]) == list:
                        await message.channel.send(random.choice(data[i]))
                    else:
                        await message.channel.send(data[i])
                else:
                    return await message.add_reaction(random.choice(['⌚','⏳','⏰','🕛','🕐','🕖','🕕','🕔','🕚','🕙','🕓','🕒','🕗','🕑']))
                return self.dt.update({message.guild.id: {message.author.id: datetime.utcnow()}})


    @commands.command(name='atk_list', aliases=['atk_list_all','atk_list_all_atks','list_atk','listatk'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def atk_list(self, ctx) -> None:
        cog = self.client.get_cog('Help')
        await ctx.invoke(cog.atk_help)

    @atk_list.error
    async def atk_list_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'{self.config["emotes"]["ERROR"]} You are on cooldown for next {error.retry_after}')
        else:
            await ctx.reply("Some unexpected error occured")
            raise error

    @commands.command()
    @commands.is_owner()
    async def pignore(self, ctx):
        print(self.aignores)

    @commands.command()
    @commands.is_owner()
    async def patk(self, ctx):
        print(self.atks)

    @commands.command(aliases=['manualtrigger'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def manual_trigger(self, ctx, *, message):
        try:
            data = self.atks[str(ctx.guild.id)]
        except KeyError:
            self.atks.update({str(ctx.guild.id): {}})
            data = self.atks[str(ctx.guild.id)]

        try:
            await ctx.send(data[message])
        except KeyError:
            await ctx.send(f'{self.config["emotes"]["ERROR"]} No such atk found')

    @manual_trigger.error
    async def manual_trigger_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'{self.config["emotes"]["ERROR"]} You are on cooldown for next {round(error.retry_after,2)} seconds.')
        else:
            await ctx.reply(f"{self.config['emotes']['ERROR']} Error: Some unexpected error occured")
            raise error

def setup(client):
    client.add_cog(ATK(client))
