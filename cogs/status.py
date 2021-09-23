from random import randint
import discord, requests, datetime
from discord.ext import commands
from os import path
import loggers.logger as log

class Status(commands.Cog):
    cog_name = 'Status'
    def __init__(self,client):
        self.client = client

    @commands.command(aliases=['ping'])
    async def status(self,ctx):
        name = 'Status'

        try:

            # Create date time objects
            dt = datetime.datetime.now()
            date = '{:%B %d, %Y}'.format(dt)
            time = dt.strftime("%H:%M:%S")

            # Load json file from URL
            url = 'https://discordstatus.com/api/v2/summary.json'
            status_json = requests.get(url).json()
            
            # Checks if file exist. It does so to check if bot is being hosted on my PC or not.
            if path.exists('./exist_check'):
                desc = 'Self hosted. Stable speeds.'
            else:
                desc = 'Hosted on Heroku. Expect slower speeds. Bot may crash.'
            
            # Could not find a better way to do this.
            # Assigns status string to easily workable variables
            for comps in status_json["components"]:
                if comps["name"] == "API":
                    api_status = comps["status"].capitalize()
                if comps["name"] == "Media Proxy":
                    media_proxy_status = comps["status"].capitalize()
                if comps["name"] == "Search":
                    search_status = comps["status"]
                if comps["name"] == "Push Notifications":
                    push_notifications_status = comps["status"].capitalize()
                if comps["name"] == "Brazil":
                    brazil_status = comps["status"].capitalize()
                if comps["name"] == "Europe":
                    europe_status = comps["status"].capitalize()
                if comps["name"] == "Hong Kong":
                    hong_kong_status = comps["status"].capitalize()
                if comps["name"] == "India":
                    india_status = comps["status"].capitalize()
                if comps["name"] == "Japan":
                    japan_status = comps["status"].capitalize()
                if comps["name"] == "India":
                    russia_status = comps["status"].capitalize()
                if comps["name"] == "Singapore":
                    singapore_status = comps["status"].capitalize()
                if comps["name"] == "South Africa":
                    south_africa_status = comps["status"].capitalize()
                if comps["name"] == "South Korea":
                    south_korea_status = comps["status"].capitalize()
                if comps["name"] == "Sydney":
                    sydney_status = comps["status"].capitalize()
                if comps["name"] == "US Central":
                    usc_status = comps["status"].capitalize()
                if comps["name"] == "US East":
                    use_status = comps["status"].capitalize()
                if comps["name"] == "US South":
                    uss_status = comps["status"].capitalize()
                if comps["name"] == "US West":
                    usw_status = comps["status"].capitalize()
                if comps["name"] == "CloudFlare":
                    cf_status = comps["status"].capitalize()
            
            # Gathers latency information and turns it into string
            ping = round(self.client.latency, 3)
            ping = str(ping)

            # `value` information for major systems field in embed
            ap = f'API: `{api_status}`'
            mp = f'\nMedia Proxy: `{media_proxy_status}`'
            se = f'\nSearch: `{search_status}`'
            pn = f'\nPush notifications: `{push_notifications_status}`'
            cf = f'\nCloudFlare: `{cf_status}`'
            la = f'\nLatency: `{ping[-3:]} ms`'
            major_systems = ap+mp+se+pn+cf+la

            # Footer
            footer = f'Requested on {date} at {time}'

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
            embed = discord.Embed(title='Status', description=desc, color=color)
            embed.add_field(name='Major Systems', value=major_systems)
            embed.add_field(name='Voice',value=voice) 
            embed.set_footer(text=footer)

            # Send and log
            await ctx.send(embed=embed)
            await log.event_logger(ctx,name,self.cog_name)
        
        except Exception as e:
            await ctx.send("❌ Something went wrong.")
            await log.error_logger(ctx,name,self.cog_name,e)

    @commands.command()
    async def coin(self,ctx):
        if randint(1,2) == 1:
            await ctx.send('Heads')
        else:
            await ctx.send('Tails')

def setup(client):
    client.add_cog(Status(client))