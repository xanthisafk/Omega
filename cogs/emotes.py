import discord
from discord.ext import commands
import random, requests
import loggers.logger as log
import APIs.color as rang
import APIs.emotes as et

class Emotes(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[5:].capitalize()
        self.ete = et.EmbedTextEmote()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.cog_name} Running.')

    async def get_gif(self,name: str) -> str:
        """
        Generates a random gif from waifu.pics API.
        input: name = (category) of image to get.
        output: rq = returns a URL string
        """
        url = 'https://api.waifu.pics/sfw/'+name
        rq = requests.get(url).json()
        rq = rq["url"]
        return rq

    dance_list = [
        'https://media.discordapp.net/attachments/799689564092104738/885485414905970708/tenor_7.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/885485407746261013/tenor_5.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/885485407784026162/tenor_6.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/885485406299238490/tenor_4.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/885485396622995466/tenor_2.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/885485394345467944/tenor_3.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/885485389240991764/tenor_1.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/885485378491015168/tenor_8.gif',
        'https://cdn.discordapp.com/attachments/703316133717213285/885486321081139210/ByHK_IQPb.gif',
        'https://media.discordapp.net/attachments/703316133717213285/885488989568663622/kermit-dance.gif',
        'https://media.discordapp.net/attachments/703316133717213285/886125451163107368/anime-dance_1.gif',
        'https://media.discordapp.net/attachments/703316133717213285/886162194365026354/ByhduIQP-.gif',
        'https://media.discordapp.net/attachments/703272258990374973/886448324159344720/crab-rave-mmd.gif'
    ]

    sleep_list = [
        'https://cdn.discordapp.com/attachments/799689564092104738/886127225836015616/tenor_11.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/886127210912706560/tenor_8.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/886127200728911882/tenor_10.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/886127190016675840/tenor_9.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/886127186472480808/tenor_7.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/886127176842346496/tenor_6.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/886127176385183785/tenor_5.gif',
        'https://media.discordapp.net/attachments/799689564092104738/886127174590021632/tenor_4.gif',
        'https://media.discordapp.net/attachments/799689564092104738/886127173587599390/tenor_3.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/886127158978818108/tenor_1.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/886127158647488542/tenor_2.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/886127155107463198/tenor.gif',
        'https://cdn.discordapp.com/attachments/799689564092104738/886127151181594644/tenor_12.gif',
        'https://media.discordapp.net/attachments/703316133717213285/886135952127430676/umaru-umaru-chan.gif'
    ]

    pout_list = [
        'https://cdn.discordapp.com/attachments/843508777177186334/887299073009414144/tenor_1.gif',
        'https://cdn.discordapp.com/attachments/843508777177186334/887299073428840458/tenor.gif',
        'https://cdn.discordapp.com/attachments/843508777177186334/887299078470393937/tenor_3.gif',
        'https://cdn.discordapp.com/attachments/843508777177186334/887299079741243402/tenor_2.gif',
        'https://cdn.discordapp.com/attachments/843508777177186334/887299087743995955/tenor_4.gif',
        'https://cdn.discordapp.com/attachments/843508777177186334/887299092043161610/tenor_5.gif',
        'https://cdn.discordapp.com/attachments/843508777177186334/887299099139911681/tenor_6.gif',
        'https://cdn.discordapp.com/attachments/843508777177186334/887299103409733632/tenor_7.gif'
    ]

    vibe_list = [
        'https://media.giphy.com/media/bZuUnCvOSv3CTKleRz/giphy.gif',
        'https://media.giphy.com/media/5JhiUPPbmmk25J5dPy/giphy.gif',
        'https://media.giphy.com/media/vCheMEtFNI1MoUuJsK/giphy.gif',
        'https://media.giphy.com/media/k8yxkQ9HzUDldZmqpv/giphy.gif',
        'https://media.giphy.com/media/b7Fq9oXDOPgsNLOMgF/giphy.gif',
        'https://media.giphy.com/media/TbrNlFwvkSNfLH023C/giphy.gif',
        'https://media.giphy.com/media/4klUaetpUNmkeTkeoH/giphy.gif',
        'https://media.giphy.com/media/9q1AR4VnNahfgNaKsS/giphy.gif',
        'https://media.giphy.com/media/lApANmHzBQdNsSGXOy/giphy.gif',
    ]

    @commands.command()
    async def blush(self,ctx,mentioned:discord.Member=None):
        name = 'Blush'
        short_name = name.lower()
        user1 = ctx.author.name
        try:
            user2 = mentioned.name
        except: pass
        try:
            color = await rang.get_color()

            if mentioned == None:
                
                embed = discord.Embed(title = f'{ctx.author.name} is blushing!',color=color)
            else:
                embed = discord.Embed(title=f'{ctx.author.name} is blushing at {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)
            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)


    @commands.command()
    async def dance(self,ctx,mentioned:discord.Member=None):
        name = 'Dance'
        try:
            color = await rang.get_color()

            if mentioned == None:
                embed = discord.Embed(title = f'{ctx.author.name} is dancing!',color=color)
            else:
                embed = discord.Embed(title=f'{ctx.author.name} is dancing with {mentioned.name}!',color=color)

            if random.randint(0,1) == 1:
                image = random.choice(self.dance_list)
            else:
                image = await self.get_gif(name.lower())


            embed.set_image(url=image)


            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)


    @commands.command()
    async def wave(self,ctx,mentioned:discord.Member=None):
        name = 'Wave'
        try:
            color = await rang.get_color()

            if mentioned == None:
                embed = discord.Embed(title = f'{ctx.author.name} is waving!',color=color)
            else:
                embed = discord.Embed(title=f'{ctx.author.name} is waving at {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)


    @commands.command()
    async def sleep(self,ctx):
        name = 'Sleep'
        try:
            color = await rang.get_color()

            embed = discord.Embed(title = f'{ctx.author.name} is sleeping!',color=color)

            image = random.choice(self.sleep_list)
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def vibe(self,ctx,user:discord.Member=None):
        name = 'Vibe'
        try:
            color = await rang.get_color()
            if user is None:
                embed = discord.Embed(title = f'{ctx.author.name} is vibing!',color=color)
            else:
                embed = discord.Embed(title = f'{ctx.author.name} is vibing with {user.name}!',color=color)

            image = random.choice(self.vibe_list)
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)


    @commands.command()
    async def pat(self,ctx,mentioned:discord.Member=None):
        name = 'Pat'
        short_name = name.lower()
        user1 = ctx.author.name
        user2 = mentioned.name
        try:
            color = await rang.get_color()

            embed = discord.Embed(title=f'{ctx.author.name} pats {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)


    @commands.command()
    async def cry(self,ctx,mentioned:discord.Member=None):
        name = 'Cry'
        short_name = name.lower()
        user1 = ctx.author.name
        user2 = mentioned.name
        try:
            color = await rang.get_color()

            if mentioned == None:
                embed = discord.Embed(title = f'{ctx.author.name} is crying.',color=color)
            else:
                embed = discord.Embed(title=f'{ctx.author.name} is crying at {mentioned.name}',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def pout(self,ctx,mentioned:discord.Member=None):
        name = 'Pout'
        short_name = name.lower()
        user1 = ctx.author.name
        user2 = mentioned.name
        try:
            color = await rang.get_color()

            if mentioned == None:
                embed = discord.Embed(title = f'{ctx.author.name} is pouting.!',color=color)
            else:
                embed = discord.Embed(title=f'{ctx.author.name} is pouting at {mentioned.name}!',color=color)

            image = random.choice(self.pout_list)
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def kiss(self,ctx,mentioned:discord.Member=None):
        name = 'Kiss'
        short_name = name.lower()
        user1 = ctx.author.name
        user2 = mentioned.name
        try:
            color = await rang.get_color()

            if mentioned == None:
                await ctx.send("You need to tag someoneto kiss them, dummy")
                return
            else:
                text = await self.ete.create_string(user1=user1,user2=user2,type=short_name)
            embed = discord.Embed(title=text,color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def bully(self,ctx,mentioned:discord.Member=None):
        name = 'Bully'
        short_name = name.lower()
        user1 = ctx.author.name
        user2 = mentioned.name
        try:
            color = await rang.get_color()

            if mentioned == None:
                await ctx.send("You need to tag someone to BULLY THEM! ヾ(`ヘ´)ﾉﾞ")
                return
            else:
                text = await self.ete.create_string(user1=user1,user2=user2,type=short_name)
            embed = discord.Embed(title=text,color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def cuddle(self,ctx,mentioned:discord.Member=None):
        name = 'Cuddle'
        short_name = name.lower()
        user1 = ctx.author.name
        user2 = mentioned.name
        try:
            color = await rang.get_color()

            if mentioned == None:
                await ctx.send("Here have some cuddles  ╰(*´︶`*)╯♡	")
                return
            else:
                text = await self.ete.create_string(user1=user1,user2=user2,type=short_name)
                embed = discord.Embed(title=text,color=color)

            image = await self.get_gif(short_name)
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def hug(self,ctx,mentioned:discord.Member=None):
        name = 'Hug'
        try:
            color = await rang.get_color()

            if mentioned == None:
                await ctx.send("I will hug you.. ＼(￣▽￣)／	")
                return
            else:
                embed = discord.Embed(title=f'{ctx.author.name} is hugging {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def lick(self,ctx,mentioned:discord.Member=None):
        name = 'Lick'
        try:
            color = await rang.get_color()

            if mentioned == None:
                embed = discord.Embed(title=f'{ctx.author.name} is licking... something?',color=color)
            else:
                embed = discord.Embed(title=f'{ctx.author.name} is bullying {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def Smug(self,ctx,mentioned:discord.Member=None):
        name = 'Smug'
        try:
            color = await rang.get_color()

            if mentioned == None:
                embed = discord.Embed(title=f'{ctx.author.name} is feeling smug :3',color=color)
            else:
                embed = discord.Embed(title=f'{ctx.author.name} smugs at {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def bonk(self,ctx,mentioned:discord.Member=None):
        name = 'Bonk'
        try:
            color = await rang.get_color()

            if ctx.author.id == 693118595089170553:
                if mentioned == None:
                    embed = discord.Embed(title=f'{ctx.author.name} bonked!',color=color)
                    
                else:
                    embed = discord.Embed(title=f'{ctx.author.name} is boking {mentioned.name}!',color=color)

            else:
                if mentioned == None:
                    embed = discord.Embed(title=f'{ctx.author.name} bonked!',color=color)

                elif mentioned.id == 693118595089170553:
                    embed = discord.Embed(title=f'{ctx.author.name} is boking {mentioned.name}!',color=color)

                else:
                    embed = discord.Embed(title=f'{ctx.author.name} is bonking {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command(aliases=['throw'])
    async def yeet(self,ctx,mentioned:discord.Member=None):
        name = 'Yeet'
        try:
            color = await rang.get_color()

            if mentioned == None:
                await ctx.send('Mention someone to throw!')
                return
            else:
                embed = discord.Embed(title=f'{ctx.author.name} yeets {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command(aliases=['happy'])
    async def smile(self,ctx,mentioned:discord.Member=None):
        name = 'Smile'
        try:
            color = await rang.get_color()

            if mentioned == None:
                embed = discord.Embed(title=f'{ctx.author.name} is smiling!',color=color)
            else:
                embed = discord.Embed(title=f'{ctx.author.name} is smiling at {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def highfive(self,ctx,mentioned:discord.Member=None):
        name = 'Highfive'
        try:
            color = await rang.get_color()

            if mentioned == None:
                await ctx.send("Mention someone to highfive them.")
                return
            else:
                embed = discord.Embed(title=f'{ctx.author.name} highfives {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command(aliases=['hold'])
    async def handhold(self,ctx,mentioned:discord.Member=None):
        name = 'Handhold'
        try:
            color = await rang.get_color()

            if mentioned == None:
                await ctx.send("Mention someone to hold their hands.. ")
                return
            else:
                embed = discord.Embed(title=f'{ctx.author.name} is holding {mentioned.name} hands!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command(aliases=['hungry'])
    async def eat(self,ctx,mentioned:discord.Member=None):
        name = 'Nom'
        try:
            color = await rang.get_color()

            if mentioned == None:
                embed = discord.Embed(title=f'{ctx.author.name} is eating',color=color)
            else:
                embed = discord.Embed(title=f'{ctx.author.name} is eating with {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command(aliases=['nom'])
    async def bite(self,ctx,mentioned:discord.Member=None):
        name = 'Bite'
        try:
            color = await rang.get_color()

            if mentioned == None:
                await ctx.send("Mention someone to bite them.")
                return
            else:
                embed = discord.Embed(title=f'{ctx.author.name} is biting {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command(aliases=['superhug'])
    async def glomp(self,ctx,mentioned:discord.Member=None):
        name = 'Glomp'
        try:
            color = await rang.get_color()

            if mentioned == None:
                await ctx.send("Mention someone pls. Glomping is worth it.")
                return
            else:
                embed = discord.Embed(title=f'{ctx.author.name} glomps {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def slap(self,ctx,mentioned:discord.Member=None):
        name = 'Slap'
        try:
            color = await rang.get_color()

            if mentioned == None:
                await ctx.send("To slap someone you need to mention them 😩")
                return
            else:
                embed = discord.Embed(title=f'{ctx.author.name} slaps {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def kill(self,ctx,mentioned:discord.Member=None):
        name = 'Kill'
        try:
            color = await rang.get_color()

            if mentioned == None:
                await ctx.send("Kill who? Mention them ples")
                return
            else:
                embed = discord.Embed(title=f'{ctx.author.name} kills {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def kick(self,ctx,mentioned:discord.Member=None):
        name = 'Kick'
        try:
            color = await rang.get_color()

            if mentioned == None:
                await ctx.send("You can not kick air!! Mention someone!")
                return
            else:
                embed = discord.Embed(title=f'{ctx.author.name} kicks {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def wink(self,ctx,mentioned:discord.Member=None):
        name = 'Wink'
        try:
            color = await rang.get_color()

            if mentioned == None:
                embed = discord.Embed(title=f'{ctx.author.name} winks!',color=color)
            else:
                embed = discord.Embed(title=f'{ctx.author.name} winks at {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def poke(self,ctx,mentioned:discord.Member=None):
        name = 'Poke'
        try:
            color = await rang.get_color()

            if mentioned == None:
                await ctx.send("Who tf do I poke? Mention them")
                return
            else:
                embed = discord.Embed(title=f'{ctx.author.name} is poking {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def cringe(self,ctx,mentioned:discord.Member=None):
        name = 'Cringe'
        try:
            color = await rang.get_color()

            if mentioned == None:
                embed = discord.Embed(title=f'{ctx.author.name} is cringing',color=color)
            else:
                embed = discord.Embed(title=f'{ctx.author.name} cringes at {mentioned.name}!',color=color)

            image = await self.get_gif(name.lower())
            embed.set_image(url=image)

            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)

        except Exception as e:
            await ctx.send('Something went wrong.')
            await log.error_logger(ctx,name,self.cog_name,e)

def setup(client):
    client.add_cog(Emotes(client))
