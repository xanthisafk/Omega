import discord
from discord.ext import commands
import json, os, random,re
import loggers.logger as log

class ATK(commands.Cog):
    cog_name = 'ATK'
    def __init__(self,client):
        self.client = client

        ignored_data = {"Ignored": []}

        if not os.path.exists('./files/ignore_list.json'):
            f = open('files/ignore_list.json', "w")
            json.dump(ignored_data,f,indent=4)

        new_data= {}
        if not os.path.exists('./files/list.json'):
            f = open('files/list.json', "w")
            json.dump(new_data,f,indent=4)

    @commands.command()
    async def ignore(self,ctx):
        command_name = 'Ignore'
        try:
            id = ctx.author.id

            with open('files/ignore_list.json', "r") as js:
                data = json.load(js)
                js.close()

            if id in data['Ignored']:
                await ctx.send('❌ Error: You are already on list.')
                return

            data['Ignored'].insert(0,id)

            with open('files/ignore_list.json', 'w') as js:
                json.dump(data,js,indent=4)
                js.close()
                await ctx.send("✅ Success: You are added to list")
            
            await log.event_logger(ctx,command_name,self.cog_name)

        except Exception as e:
            await ctx.send("Something went wrong")
            print(e)
            await log.error_logger(ctx,command_name,self.cog_name,e)
        
        
    
    @commands.command()
    async def unignore(self,ctx):
        command_name = 'Unignore'
        try:
            id = ctx.author.id

            with open('files/ignore_list.json', "r") as js:
                data = json.load(js)
                js.close()
            
            if id not in data["Ignored"]:
                await ctx.send("❌ Error: You are not in ignore list.")
                return

            data['Ignored'].remove(id)

            with open('files/ignore_list.json', 'w') as js:
                json.dump(data,js, indent=4)
                js.close()
                await ctx.send("✅ Success: You are removed from ignore list.")

            await log.event_logger(ctx,command_name,self.cog_name)

        except Exception as e:
            await ctx.send("Something went wrong")
            print(e)
            await log.error_logger(ctx,command_name,self.cog_name,e)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_atk(self, ctx, *, string:str) -> None :
        command_name = 'Add_ATK'
        try:

            x = string.split(",",1)
            try:
                name = x[0].rstrip()
                url = x[1]
            except Exception as e:
                if isinstance(e,IndexError):
                    await ctx.send("Please enter in format of `text1, text2` (Comma is important)")
                    return

            name = name.lower()
            to_add = {name:url}

            with open('files/list.json', 'r') as js:
                data = json.load(js)
                js.close()

            if name in data:
                await ctx.send("❌ Error: Name already bound")

            data.update(to_add)

            with open('files/list.json', 'w') as js:
                json.dump(data,js,indent=4)
                js.close()
                await ctx.send(f'✅ Success: {name} is now bound.')

            await log.event_logger(ctx,command_name,self.cog_name)

        except Exception as e:
            
            await ctx.send("Something went wrong")
            print(e)
            await log.error_logger(ctx,command_name,self.cog_name,e)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_atk(self, ctx, *, name: str,) -> None :
        command_name = 'Remove_ATK'
        try:
            with open('files/list.json', 'r') as js:
                    data = json.load(js)
                    js.close()
            
            name = name.lower()
            if name in data:
                del data[name]
            else:
                await ctx.send(f'❌ Error: {name} not found.')
                return

            with open('files/list.json', 'w') as js:
                json.dump(data,js,indent=4)
                js.close()
                await ctx.send(f'✅ Success: {name} was removed.')

            await log.event_logger(ctx,command_name,self.cog_name)
        
        except Exception as e:
            await ctx.send("Something went wrong")
            print(e)
            await log.error_logger(ctx,command_name,self.cog_name)



    @commands.Cog.listener()
    async def on_message(self,message):

        with open('files/ignore_list.json','r') as js:
            data = json.load(js)
            js.close()
        
        if message.author == self.client.user or message.author.bot == True or message.author.id in data["Ignored"]: return

        with open('files/list.json','r') as js:
            idk = json.load(js)
            js.close()
        
        s = message.content.lower()

        
        split_s = s.split(' ')
        if s.startswith('>') : return
        for word in split_s:
            if word.startswith(':') or word.startswith('>') or word.startswith('-'): return
            if re.search(r'\bnooooo',word): 
                await message.channel.send(random.choice(idk['nooooo']))
                await log.event_logger(message,word,self.cog_name); return
        
        try:
            for word in idk:
                check1 = r":"+word+r":"
                check2 = r"\b-"+word+r"\b"
                check3 = r"\b>"+word+r"\b"
                if re.search(check1,s) or re.search(check2,s) or re.search(check3,s) : return
                regex_string = r"\b"+word+ r"\b"
                if re.search(regex_string,s):
                    if type(idk[word]) == list:
                        await message.channel.send(random.choice(idk[word]))
                        await log.event_logger(message,word,self.cog_name)
                        return
                    else:
                        await message.channel.send(idk[word])
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