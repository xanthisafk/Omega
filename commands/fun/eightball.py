import asyncio
import random

import APIs.color as rang
import discord
from discord.ext import commands

from loggers.logger import logger


class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:].capitalize()
        

    @commands.command(name='8ball')
    async def ball_8(self, ctx, *, question: str = None) -> None:

        name = '8ball'

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

        if question is None:
            await ctx.send("You need to ask a question for 🎱 to work.")
            return

        color = await rang.get_color()

        desc = {
            1: "🎱 Asking 8Ball...",
            2: "And... 🎱 says..",
            3: "And 🎱 says: "
        }

        embed = discord.Embed(
            title=f'{ctx.author} asked: "{question}"', description=(desc[1]), color=color)
        message = await ctx.reply(embed=embed)
        await asyncio.sleep(random.randint(1, 3))

        embed = discord.Embed(
            title=f'{ctx.author} asked: "{question}"', description=(desc[2]), color=color)
        await message.edit(embed=embed)
        await asyncio.sleep(random.randint(1, 3))

        embed = discord.Embed(title=f'{ctx.author} asked: "{question}"', description=(
            desc[3]+random.choice(ball8)), color=color)
        await message.edit(embed=embed)
        await logger.logger(ctx,name,self.cog_name,'INFO')


def setup(bot):
    bot.add_cog(EightBall(bot))
