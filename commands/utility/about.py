import os

import APIs.color as rang
import discord
import loggers.logger as log
from discord.ext import commands

class About(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[9:].capitalize()

    async def emo_count(self):
        count = 0
        cog = self.client.get_cog('Emotes')
        cmd = cog.get_commands()
        for i in cmd:
            for _ in i.aliases:
                count += 1
        return count

    async def atk_count(self):
        count = 0
        cog = self.client.get_cog('ATK')
        for _ in cog.atks:
            count += 1
        return count

    @commands.command()
    async def about(self, ctx):
        command_name = ctx.command.name.capitalize()
        cog_name = ctx.command.cog_name.capitalize()

        # try:
        color = await rang.get_color()

        servers = len(self.client.guilds)

        people = 0
        for guild in self.client.guilds:
            people += guild.member_count

        cog_amount = 0
        for dir in os.listdir('./commands'):
            for _ in os.listdir(f'./commands/{dir}'):
                cog_amount += 1

        command_amount = 0
        for _ in self.client.commands:
            command_amount += 1
        command_amount += (await self.emo_count())

        atk_count = await self.atk_count()

        tot_s = f'Currently in {servers} servers and working with {people} people.\n'
        tot_c = f'{command_amount+1} commands are loaded across {cog_amount} extensions.\n'
        tot_a = f'{atk_count} auto trigger keywords are loaded.'
        field_val = tot_s+tot_c+tot_a

        footer = f'v1.0.1 - Made by Xanthis!'

        thumb = self.client.user.avatar_url

        embed = discord.Embed(
            title='About', description='Discord bot, written in Python, uses `discord.py`', color=color)
        embed.add_field(name='Usage', value=field_val, inline=False)
        embed.set_footer(text=footer)
        embed.set_thumbnail(url=thumb)
        await ctx.reply(embed=embed)
        await log.logger(ctx, command_name, cog_name,"INFO")


def setup(client):
    client.add_cog(About(client))
