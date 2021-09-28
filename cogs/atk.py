import discord
from discord.ext import commands
import random, re, config
import loggers.logger as log
import files.db as pql

class ATK(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.cog_name = __name__[5:].capitalize()
        self.p = pql.PostgreSQL(DB_HOST=config.DB_HOST,DB_USER=config.DB_USER,DB_PASS=config.DB_PASS,DB_NAME=config.DB_NAME)

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
        self.aatk = await self.get_new_atks()
        self.aignores = await self.get_new_ignores()
        print(f'{self.cog_name} Running.')


    # get new atks list
    async def get_new_atks(self) -> list:
        """
        Function that retrives a new list of updated ATK list and assigns it to global variable

        agrs:
            None
        returns:
            self.aatk: list -> List of all available ATKs currently registered
        """
        string = "SELECT name FROM atks"
        atks = await self.p.execute(string)

        self.aatk = []
        length = len(atks)-1

        for i in range(0,length):
            self.aatk.append(atks[i][0])

        return self.aatk
    
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
            length+=1

        for i in range(0,length):
            self.aignores.append(ignores[i][0])

        return self.aignores


    @commands.command(aliases=["atk_ignore"])
    async def ignore(self,ctx:commands.Context) -> None:
        """
        Adds the user to a list of ignored users. People who use this function no longer trigger ATKs.

        args:
            ctx: commands.Context -> ctx given by Discord library
        returns:
            None (Adds user to database)
        """
        command_name = "Ignore"
        try:
            id = str(ctx.author.id)

            data = self.aignores

            if id in data:
                await ctx.send('❌ Error: You are already on list.')
                return
            
            await self.p.insert(table='ignores',fields='id',values=id)
            await self.p.commit()
            await self.get_new_ignores()
            await ctx.send("✅ Success: You are added to list")
            await log.event_logger(ctx,command_name,self.cog_name)

        except Exception as e:
            await ctx.send("Something went wrong")
            print(e)
            await log.error_logger(ctx,command_name,self.cog_name,e)
        
        
    
    @commands.command(aliases=["atk_unignore"])
    async def unignore(self,ctx: commands.Context) -> None:
        """
        Removes id of user from list of ignored people.

        args:
            ctx: commands.Context -> ctx given by Discord library
        :returns
            None (removes user from database)
        """
        command_name = 'Unignore'
        try:
            id = str(ctx.author.id)

            
            if id not in self.aignores:
                await ctx.send("❌ Error: You are not in ignore list.")
                return

            string = f"DELETE FROM ignores WHERE id = '{id}'"
            await self.p.execute(string)
            await self.p.commit()
            await self.get_new_ignores()
            await ctx.send("✅ Success: You are removed from ignore list.")
            await log.event_logger(ctx,command_name,self.cog_name)

        except Exception as e:
            await ctx.send("Something went wrong")
            print(e)
            await log.error_logger(ctx,command_name,self.cog_name,e)

    @commands.command(aliases=["atk_add"])
    @commands.has_permissions(administrator=True)
    async def add_atk(self, ctx: commands.Context, *, string:str) -> None :
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

            x = string.split(",",1)
            try:
                name = x[0].rstrip()
                url = x[1]
                if len(url) > 255:
                    await ctx.send("Value must be under 255 characters.")
                    return
            except Exception as e:
                if isinstance(e,IndexError):
                    await ctx.send("Please enter in format of `text1, text2` (Comma is important)")
                    return

            name = name.lower()
            
            if name in self.aatk:
                await ctx.send(f"❌ Error: `{name}` already bound")
                return

            string = f"INSERT INTO atks(name,value) VALUES('{name}','{url}')"
            await self.p.execute(string)
            await self.p.commit()
            await self.get_new_atks()
            await ctx.send(f'✅ Success: `{name}` is now bound.')
            await log.event_logger(ctx,command_name,self.cog_name)

        except Exception as e:
            
            await ctx.send("Something went wrong.")
            print(e)
            await log.error_logger(ctx,command_name,self.cog_name,e)

    @commands.command(aliases=["atk_remove","atk_delete"])
    @commands.has_permissions(administrator=True)
    async def remove_atk(self, ctx, *, name: str,) -> None :
        command_name = 'Remove_ATK'
        try:
            
            name = name.lower()
            if name in self.aatk:
                string = f"DELETE FROM atks WHERE name='{name}'"
            else:
                await ctx.send(f'❌ Error: `{name}` not found.')
                return

            await self.p.execute(string)
            await self.p.commit()
            await self.get_new_atks()
            await ctx.send(f"✅ Success: `{name}` is removed")
            await log.event_logger(ctx,command_name,self.cog_name)
        
        except Exception as e:
            await ctx.send("Something went wrong")
            print(e)
            await log.error_logger(ctx,command_name,self.cog_name)



    @commands.Cog.listener()
    async def on_message(self,message):
        
        if message.author == self.client.user or message.author.bot == True or str(message.author.id) in self.aignores: return
        
        s = message.content.lower()

        split_s = s.split(' ')
        if s.startswith('>') : return
        for word in split_s:
            if word.startswith(':') or word.startswith('>') or word.startswith('-'): return
            if re.search(r'\bnooooo',word): 
                to_send = await self.p.fetch("SELECT value FROM atks WHERE name = 'nooooo'")

                await message.channel.send(random.choice(to_send[0][0]))
                await log.event_logger(message,word,self.cog_name); return
        
        try:
            for word in self.aatk:
                check1 = r":"+word+r":"
                check2 = r"\b-"+word+r"\b"
                check3 = r"\b>"+word+r"\b"
                if re.search(check1,s) or re.search(check2,s) or re.search(check3,s) : return
                regex_string = r"\b"+word+ r"\b"
                if re.search(regex_string,s):
                    if type(self.aatk[0]) == list:
                        to_send = await self.p.fetch(f"SELECT value FROM atks WHERE name = '{word}'")
                        await message.channel.send(random.choice(to_send[0][0]))
                        await log.event_logger(message,word,self.cog_name)
                        return
                    else:
                        to_send = await self.p.execute(f"SELECT value FROM atks WHERE name = '{word}'")
                        await message.channel.send(to_send[0][0])
                        await log.event_logger(message,word,self.cog_name)
                        return
                    
        except Exception as e:

            if isinstance(e,IndexError):
                await message.channel.send("Please enter in format of `text1, text2` (Comma is important)")
            else:
                await message.channel.send('Something went wrong.')
                print(e)
                await log.error_logger(message,s,self.cog_name,e)
                raise e

        for x in message.mentions:
                if(x==self.client.user):
                    if random.randrange(1,10) == 7:
                        await message.channel.send('I\'m busy right now:')
                        await message.channel.send('https://media.discordapp.net/attachments/845191720224161824/889751939053682748/coom.png')
                        if random.randrange(1,100) == 89:
                            await message.channel.send('p/s: blame Navi.')
                        s = 'Mentioned'
                        await log.event_logger(message,s,self.cog_name)
                    else:
                        return

def setup(client):
    client.add_cog(ATK(client))