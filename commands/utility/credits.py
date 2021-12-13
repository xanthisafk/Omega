import asyncio
import discord, APIs.color as rang
from discord.ext import commands
import json
import codecs


class Credits(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]
        with codecs.open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.error_emote = config['emotes']['ERROR']
            self.emote_left = config['emotes']['LEFT']
            self.emote_right = config['emotes']['RIGHT']
            self.owner = config['general']['OWNER']
            config = None

    @commands.command(aliases=['credit'])
    async def credits(self, ctx):
        color =  await rang.get_color()
        embed = discord.Embed(title='Credits', color =  color)
        omega= r"""
█▀▀█ █▀▄▀█ █▀▀ █▀▀▀ █▀▀█ 
█──█ █─▀─█ █▀▀ █─▀█ █▄▄█ 
▀▀▀▀ ▀───▀ ▀▀▀ ▀▀▀▀ ▀──▀
"""

        about = f"""{omega}
        Made by Xanthis. (cupnoodle#3924)
This bot uses [discord.py](https://github.com/rapptz/discord.py) Python library.
This bot's owner(s) are set to:"""

        j=1
        for i in self.owner:
            about+= f'\n{j}.\t<@{i}>'
            j+=1
        
        embed.add_field(name='General details',value=about)


        apis = """**Emote GIFs**
[Waifu.pics](https://waifu.pics)
[Nekos.best](https://nekos.best)
[Giphy](https://giphy.com)
[Tenor](https://tenor.com)

**Fun**
[icanhazdadjoke](https://icanhazdadjoke.com) (puns)

**Animals**
[Dog.ceo](https://dog.ceo/) (Dog photos)
[Random.cats](https://random.cats) (Cat photos)
[Randomfox.ca](https://randomfox.ca) (Fox photos)
[random-d.uk](https://random-d.uk) (Duck photos)
[Some Random Api](https://some-random-api.ml) (Bird, Koala, Panda, Racoon photos)

**Utility**
[DiscordStatus.com](https://discordstatus.com) (Discord status)"""

        libs =  """**In no particular order**
[aiohttp](https://docs.aiohttp.org/en/stable/)
[discord.py](https://github.com/Rapptz/discord.py)
[emojifier](https://github.com/MakufonSkifto/Emojifier)
[psycopg2](https://www.psycopg.org/docs/)
[requests](https://docs.python-requests.org/en/latest/)
[text-to-owo](https://github.com/piethrower/OwO)
[Pillow](https://pypi.org/project/Pillow/)
[pyfiglet](https://github.com/pwaller/pyfiglet)
[wavelink](https://github.com/PythonistaGuild/Wavelink)
[redditeasy](https://pypi.org/project/redditeasy/)"""

        message = await ctx.reply(embed=embed)

        right_e = self.emote_right
        left_e = self.emote_left
        error_e = self.emote_error

        total = 3
        min = 1
        current = 1

        await message.add_reaction(left_e)
        await message.add_reaction(right_e)
        await message.add_reaction(error_e)

        def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in [left_e, right_e, error_e]
        
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30, check=check)

                embed.remove_field(0)

                if str(reaction.emoji) == right_e and current != total:
                    current+=1
                elif str(reaction.emoji) == left_e and current > min:
                    current-=1
                elif str(reaction.emoji) == error_e:
                    await message.clear_reactions()
                    break
                elif current == total or current == 0:
                    pass
                
                
                if current == 1:
                    embed.add_field(name='General details',value=about)
                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)

                elif current == 2:
                    embed.add_field(name='APIs',value=apis)
                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)
                
                elif current == 3:
                    embed.add_field(name='Dependencies',value=libs)
                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)
                
                else:
                    await message.remove_reaction(reaction, user)


            except asyncio.TimeoutError:
                await message.clear_reaction(right_e)
                await message.clear_reaction(left_e)
                return await message.edit(content="Message timed out")

    @credits.error
    async def credits_error(self, ctx, error):
        await ctx.send(f'An unxpected error occured')
        raise error

def setup(bot):
    bot.add_cog(Credits(bot))
