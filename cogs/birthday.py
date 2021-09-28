import discord
from discord.ext import commands, tasks

import datetime

class Birthday(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[5:].capitalize()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.cog_name} Running.')

    @commands.command()
    async def lelw(self, ctx):
        embed = discord.Embed(title='lmfaoooooo')
        embed.set_footer(text='i\'m dead')
        embed.set_image(url = 'https://cdn.discordapp.com/emojis/787709636479942656.png?v=1')
        await ctx.send(embed = embed)
    

    @tasks.loop(seconds = 1)
    async def print_birthday(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if(current_time == '15:05:00'):
            await self.send_birthday()
            return 0
    
    async def send_birthday(self):
        channel =  self.client.get_channel(703316133717213285)
        await channel.send('Happy birthday <@538338456074715136>! 💃💃🥳🎉🎊')
        await channel.send('https://media.discordapp.net/attachments/843508777177186334/886181309930688532/sexy-hot.gif')
        print('sent')
        self.print_birthday.stop()

    @commands.command()
    async def start(self):
        print('starting')
        self.print_birthday.start()

    @commands.command()
    async def birthday(self,ctx):
        embed = discord.Embed(title='Happy birthday', color = 0x551A8B)
        embed.set_image(url='https://media.giphy.com/media/bZuUnCvOSv3CTKleRz/giphy.gif')
        await ctx.send(embed=embed)
        




def setup(client):
    client.add_cog(Birthday(client))