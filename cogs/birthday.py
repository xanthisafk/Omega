import discord
from discord.ext import commands, tasks
import files.color as rang

import datetime

class Birthday(commands.Cog):

    def __init__(self, client):
        self.client = client


    @tasks.loop(seconds=1)
    async def birthday_timer(self):

    	now = datetime.datetime.now()
    	time = now.strftime("%H:%M:%S")

    	if(time == '00:00:00'):
    		await self.send_birthday()
    		return 0

    async def send_birthday(self):
    	channel_id = 703316133717213285
    	channel = self.client.get_channel(channel_id)
    	await channel.send('happy Birthday!')
    	print('sent')
    	self.birthday_timer.stop()

    @commands.command()
    async def start(self):
    	print('Starting')
    	self.birthday_timer.start()

    @commands.command()
    async def birthday(self,ctx):
    	embed = discord.Embed(title='Happy birthday',color = await rang.get_color())
    	await ctx.send(embed=embed)


def setup(client):
	client.add_cog(Birthday(client))