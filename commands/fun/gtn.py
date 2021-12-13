import discord
from discord.ext import commands
import asyncio, random
import APIs.color as rang


class Guessthenumber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]

    @commands.command(name="guessthenumber", aliases=[ "gtn"])
    async def numberguessergame(self, ctx, diff: str = 'easy'):
        name = 'GuessTheNumber'
        color = await rang.get_color()

        tries = 1
        err = 1
        r1 = random.randint(1,100)
        diff.lower()

        if diff in ['easy', 'e', 'ez']: 
            r2=  10
        elif diff in ['medium', 'm']: 
            r2=  50
        elif diff in ['hard', 'h']: 
            r2=  100

        num = random.randint(r1,(r1+r2))
        embed = discord.Embed(title="Guess the number game.", description=f'Guess a  number between {r1} and {r1+r2}', color = color)
        embed.set_footer(text='You have 5 turns to guess.')
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        message = await ctx.reply(embed=embed)

        def check(author):
            def inner_check(message): 
                if message.author != author:
                    return False
                try: 
                    int(message.content) 
                    return True 
                except ValueError: 
                    return False
            return inner_check

        try:
            for i in range(5):
                try:
                    response = await self.bot.wait_for('message', timeout = 60, check=check(ctx.author))

                    guess = int(response.content)
                    

                    if guess > num:
                        embed.add_field(name=f"Guess {tries}", value=f"Your number is bigger.\nYou guessed: {guess}", inline=False)
                        embed.set_footer(text=f"{4-i} turns remain.")
                        await message.edit(embed=embed)

                    elif guess < num:
                        embed.add_field(name=f"Guess {tries}", value=f"Your number is smaller.\nYou guessed: {guess}", inline=False)
                        embed.set_footer(text=f"{4-i} turns remain.")
                        await message.edit(embed=embed)

                    elif guess == num:
                        embed.add_field(name=f"Guess {tries}", value="You got it!", inline=False)
                        embed.set_footer(text=f"It took you {tries} attempts!")
                        await message.edit(embed=embed)
                        await message.edit(content="Game over!")
                        break

                    tries += 1

                    if i == 4:
                        embed.set_footer(text='You are out of moves! You lose.')
                        await message.edit(embed=embed)
                        await message.edit(content="Game over!")
                        break

                except Exception as e:
                    if isinstance(e,ValueError):
                        embed.add_field(name=f"Error {err}", value="Please enter a number", inline=False)
                        await message.edit(embed=embed)
                        err += 1
                        if err == 3:
                            break
                        else:
                            pass

        except asyncio.TimeoutError:
                await message.edit(content="Message timed out!")

def setup(bot):
    bot.add_cog(Guessthenumber(bot))
