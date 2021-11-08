import datetime

import discord
from discord.ext import commands, tasks

import APIs.color as rang
import loggers.logger as log
import config


class Birthday(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[9:]

    @tasks.loop(seconds=1)
    async def print_birthday(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if(current_time == '15:05:00'):
            await self.send_birthday()
            return

    async def send_birthday(self):
        channel = self.client.get_channel(703316133717213285)
        await channel.send('Happy birthday <@538338456074715136>! 💃💃🥳🎉🎊')
        await channel.send('https://media.discordapp.net/attachments/843508777177186334/886181309930688532/sexy-hot.gif')
        self.print_birthday.stop()

    @commands.command()
    async def start(self):
        print('starting')
        self.print_birthday.start()

    @commands.command()
    async def birthday(self, ctx):
        color = rang.get_color()
        name = 'Birthday'
        embed = discord.Embed(title='Happy birthday', color=color)
        embed.set_image(url='https://c.tenor.com/eDfWpD2K5m0AAAAC/hideri-anime.gif')
        await ctx.reply(embed=embed)
        await log.logger(ctx,name,self.cog_name,'INFO')

    @start.error
    async def start_error(self,ctx,err):
        await ctx.send(f"{config.EMOTE_ERROR} Something unexpected happened.")
        raise err

    @birthday.error
    async def birthday_error(self,ctx,err):
        await ctx.end(f"{config.EMOTE_ERROR} Something unexpected happened.")
        raise err


def setup(client):
    client.add_cog(Birthday(client))
