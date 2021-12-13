import os
from datetime import datetime, timedelta

import APIs.color as rang
import discord
from discord.ext import commands

class About(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[9:].capitalize()
        self.error_emote = self.client.config['emotes']['ERROR']

    async def emo_count(self):
        count = 0
        cog = self.client.get_cog('Emotes')
        cmd = cog.get_commands()
        for i in cmd:
            for _ in i.aliases:
                count += 1
        return count

    async def atk_count(self):
        server = 0
        atk = 0
        cog = self.client.get_cog('ATK')
        for i in cog.atks:
            for _ in cog.atks[i]:
                atk += 1
            server += 1
        
        count = [server, atk]

        return count

    @commands.command()
    async def about(self, ctx):

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
        tot_a = f'{atk_count[1]} auto trigger keywords are loaded across {atk_count[0]} servers.'
        field_val = tot_s+tot_c+tot_a

        footer = f'v1.2 - Made by Xanthis!'

        thumb = self.client.user.avatar_url

        embed = discord.Embed(
            title='About', description='discord bot, written in Python, uses `discord.py`', color=color)
        embed.add_field(name='Usage', value=field_val, inline=False)
        embed.set_footer(text=footer)
        embed.set_thumbnail(url=thumb)
        await ctx.reply(embed=embed)

    @about.error
    async def about_error(self,ctx,error):
        await ctx.reply(f'{self.emote_error} An unexpected error occured.')
        raise error

    @commands.command(aliases=['whoami'])
    async def whois(self, ctx, user:discord.Member=None):

        if user is None:
            user:discord.Member = ctx.author

        embed = discord.Embed(color = user.color, timestamp=datetime.now())

        embed.set_author(name=str(user),icon_url=user.avatar_url)

        embed.set_thumbnail(url=user.avatar_url)

        embed.add_field(name="🤖 Is Bot", value=user.bot)

        embed.add_field(name='✒ Nickname', value=str(user.nick))

        embed.add_field(name="🖥 Is System", value=user.system)

        permissions = ''

        if user.guild_permissions.administrator:
            permissions = "Administrator"

        else:
            for permission in user.guild_permissions:
                if permission[1]:
                    permissions += permission[0].replace('_', ' ') + ", "
            permissions = permissions.capitalize()[:-2]

        embed.add_field(name="👨‍💼 Permissions", value=permissions, inline=False)

        roles = ''

        for role in user.roles:
            if role.is_default():
                pass
            roles += role.mention + ", "
        roles = roles[:-2]

        embed.add_field(name="💼 Roles", value=roles, inline=False)

        jtime = user.joined_at
        ctime = user.created_at

        joindiff:timedelta = datetime.now() - jtime
        creatediff:timedelta = datetime.now() - ctime

        jtime = f"{jtime} ({joindiff.days} days ago)"
        ctime = f"{ctime} ({creatediff.days} days ago)"


        embed.add_field(name="🛠 Account created on", value=ctime)
        embed.add_field(name="🚪 Joined server on", value=jtime)

        embed.set_footer(text=user.id)

        await ctx.send(embed=embed)

    @whois.error
    async def whois_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            return await ctx.send(f"{self.error_emote} User `{error.argument}` not found.")
        await ctx.send(f"{self.error_emote} An unexpected error occured.")
        raise error

    @commands.command(aliases=['si'])
    async def serverinfo(self,ctx):

        guild:discord.Guild = ctx.guild
        embed = discord.Embed(color=discord.Color.random(), timestamp=datetime.now())

        embed.set_author(name=guild.name, icon_url=guild.icon_url)
        if guild.description:
            embed.description = guild.description

        embed.set_thumbnail(url=guild.icon_url)

        embed.add_field(name="💬 Channel count", value=f'**{len(guild.channels)}**')
        embed.add_field(name="🔣 Categories", value=len(guild.categories))
        embed.add_field(name="🔊 Voice channels", value=len(guild.voice_channels))
        embed.add_field(name="💖 Emojis", value=len(guild.emojis))
        embed.add_field(name="✈ Features", value=(", ".join(guild.features)[:-2] if len(guild.features) > 0 else "None"))
        embed.add_field(name="💼 Roles", value=len(guild.roles))
        embed.add_field(name="👑 Owner", value=str(guild.owner))
        time:timedelta = datetime.now() - guild.created_at
        embed.add_field(name="🛠 Created on", value=(guild.created_at.ctime()+f"\n({time.days} days ago)"))

        try:
            embed.set_footer(text=f'{guild.id} • {await guild.vanity_invite()}')
        except:
            embed.set_footer(text=guild.id)


        await ctx.send(embed=embed)

    @serverinfo.error
    async def serverinfo_error(self,ctx,error):
        await ctx.send(f"{self.error_emote} An unexpected error occured.")



def setup(client):
    client.add_cog(About(client))
