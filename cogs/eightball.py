import random
import asyncio

import APIs.color as rang
import discord
from discord.ext import commands


class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ball8 = [
    "🟢 It is Certain.",
    "🟢 It is decidedly so.", 
    "🟢 Without a doubt", 
    "🟢 Yes definitely", 
    "🟢 You may rely on it", 
    "🟢 As I  see, yes", 
    "🟢 Most Likely", 
    "🟢 Outlook good", 
    "🟢 Yes", 
    "🟢 Signs points to yes", 
    "🟡 Reply hazy, try again", 
    "🟡 Ask again later", 
    "🟡 Better not tell you now", 
    "🟡 Cannot predict now", 
    "🟡 Concentrate and ask again", 
    "🔴 Don't count on it", 
    "🔴 My reply is no",
    "🔴 My sources say no",
    "🔴 Outlook not so good",
    "🔴 Very doubtful" 
    ]

    @commands.command(name='8ball')
    async def ball_8(self, ctx, * , question :str = None) -> None:

        if question is None:
            await ctx.send("You need to ask a question for 🎱 to work.")
            return

        color = await rang.get_color()

        desc = {
            1:"🎱 Asking 8Ball...",
            2:"And... 🎱 says..",
            3:"And 🎱 says: "
        }

        embed = discord.Embed(title = f'You asked: "{question}"',description = (desc[1]), color = color)
        message = await ctx.send(embed=embed)
        await asyncio.sleep(random.randint(1,3))

        embed = discord.Embed(title = f'You asked: "{question}"',description = (desc[2]), color = color)
        await message.edit(embed=embed)
        await asyncio.sleep(random.randint(1,3))
        
        embed = discord.Embed(title = f'You asked: "{question}"',description = (desc[3]+random.choice(self.ball8)), color = color)
        await message.edit(embed=embed)


def setup(bot):
    bot.add_cog(EightBall(bot))
