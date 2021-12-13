import datetime
from os import path

import discord
import aiohttp
from discord.ext import commands


class Status(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = __name__[9:].capitalize()

    @commands.command()
    @commands.cooldown(1,60,commands.BucketType.user)
    async def status(self, ctx):

        # Load json file from URL
        url = 'https://discordstatus.com/api/v2/summary.json'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                status_json = await response.json()
                await session.close()

        # Checks if file exist. It does so to check if bot is being hosted on my PC or not.
        if path.exists('files/exists'):
            desc = 'Self hosted. Variable speeds'
        else:
            desc = 'Hosted on Heroku. Stable speeds. Bot may crash.'

        # Could not find a better way to do this.
        # Assigns status string to easily workable variables
        for comps in status_json["components"]:
            if comps["name"] == "API":
                api_status = comps["status"].capitalize()
            elif comps["name"] == "Media Proxy":
                media_proxy_status = comps["status"].capitalize()
            elif comps["name"] == "Search":
                search_status = comps["status"]
            elif comps["name"] == "Push Notifications":
                push_notifications_status = comps["status"].capitalize()
            elif comps["name"] == "Brazil":
                brazil_status = comps["status"].capitalize()
            elif comps["name"] == "Europe":
                europe_status = comps["status"].capitalize()
            elif comps["name"] == "Hong Kong":
                hong_kong_status = comps["status"].capitalize()
            elif comps["name"] == "India":
                india_status = comps["status"].capitalize()
            elif comps["name"] == "Japan":
                japan_status = comps["status"].capitalize()
            elif comps["name"] == "Russia":
                russia_status = comps["status"].capitalize()
            elif comps["name"] == "Singapore":
                singapore_status = comps["status"].capitalize()
            elif comps["name"] == "South Africa":
                south_africa_status = comps["status"].capitalize()
            elif comps["name"] == "South Korea":
                south_korea_status = comps["status"].capitalize()
            elif comps["name"] == "Sydney":
                sydney_status = comps["status"].capitalize()
            elif comps["name"] == "US Central":
                usc_status = comps["status"].capitalize()
            elif comps["name"] == "US East":
                use_status = comps["status"].capitalize()
            elif comps["name"] == "US South":
                uss_status = comps["status"].capitalize()
            elif comps["name"] == "US West":
                usw_status = comps["status"].capitalize()
            elif comps["name"] == "CloudFlare":
                cf_status = comps["status"].capitalize()

        cog = self.client.get_cog('ATK')
        try:
            cog.redis.ping()
            db_status = 'Online'
        except:
            db_status = 'Offline'

        # Gathers latency information and turns it into string
        ping = round(self.client.latency*1000)
        ping = str(ping)

        # `value` information for major systems field in embed
        ap = f'API: `{api_status}`'
        mp = f'\nMedia Proxy: `{media_proxy_status}`'
        se = f'\nSearch: `{search_status}`'
        pn = f'\nPush notifications: `{push_notifications_status}`'
        cf = f'\nCloudFlare: `{cf_status}`'
        la = f'\nLatency: `{ping[-3:]} ms`'
        db = f'\nDatabase: `{db_status}`'
        major_systems = ap+mp+se+pn+cf+db+la

        # String for voice channels
        br = f'🇧🇷 Brazil: `{brazil_status}`'
        eu = f'\n🇪🇺 Europe: `{europe_status}`'
        hk = f'\n🇭🇰 Hong Kong: `{hong_kong_status}`'
        bh = f'\n🇮🇳 India: `{india_status}`'
        jp = f'\n🇯🇵 Japan: `{japan_status}`'
        ru = f'\n🇷🇺 Russia: `{russia_status}`'
        si = f'\n🇸🇬 Singapore: `{singapore_status}`'
        sa = f'\n🇿🇦 South Africa: `{south_africa_status}`'
        sk = f'\n🇰🇷 South Korea: `{south_korea_status}`'
        sy = f'\n🇦🇺 Sydney: `{sydney_status}`'
        uc = f'\n🇺🇸 US Central: `{usc_status}`'
        ue = f'\n🇺🇸 US East: `{use_status}`'
        us = f'\n🇺🇸 US South: `{uss_status}`'
        uw = f'\n🇺🇸 US West: `{usw_status}`'
        voice = br+eu+hk+bh+jp+ru+si+sa+sk+sy+uc+ue+us+uw

        # Color for embed depending on how the API is doing
        if api_status == "Operational":
            color = 0x00FF00
        elif api_status == "Partial Outage":
            color = 0xFFFF00
        elif api_status == "Major Outage":
            color = 0xFF0000

        # Create embed
        embed = discord.Embed(
            title='Status', description=desc, color=color, timestamp = datetime.datetime.utcnow())
        embed.add_field(name='Major Systems', value=major_systems)
        embed.add_field(name='Voice', value=voice)
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @status.error
    async def status_error(self, ctx, error):
        await ctx.send("An unexpected error occured.")
        raise error

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Pong!"""
        await ctx.send(f'Pong! {round(self.client.latency*1000)}ms')

    @ping.error
    async def ping_error(self, ctx, error):
        await ctx.send("An unexpected error occured.")
        raise error

def setup(client):
    client.add_cog(Status(client))
