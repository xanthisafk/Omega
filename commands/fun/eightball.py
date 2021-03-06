import asyncio
import random

import APIs.color as rang
import discord
from discord.ext import commands

import codecs, json

class MissingQuestion(Exception):
    def __init__(self):
        super().__init__(f'You need to ask a question for 🎱 to work.')


class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]
        with codecs.open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.error_emote = config['emotes']['ERROR']
            config = None


    @commands.command(name='8ball')
    @commands.cooldown(1, 10, commands.BucketType.user)
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
            raise MissingQuestion()

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

    @ball_8.error
    async def ball_8_error(self, ctx, error):
        if isinstance(error,commands.CommandInvokeError):
            if isinstance(error.original, MissingQuestion):
                await ctx.send(f'{self.error_emote} Error: {error.original}')
        elif isinstance(error,commands.CommandOnCooldown):
            return await ctx.send(f'{self.error_emote} Command is on cooldown. Try again in {round(error.retry_after,1)} seconds.')

        else: 
            await ctx.send(f'{self.error_emote} An error has occured.')
            raise error

def setup(bot):
    bot.add_cog(EightBall(bot))
