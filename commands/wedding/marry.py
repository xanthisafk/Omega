import discord
from discord.ext import commands
import asyncio
import redis

class Wedding(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.emotes = self.client.config["emotes"]
        cog = self.client.get_cog("ATK")
        self.redis = cog.redis

    @commands.command()
    async def marry(self, ctx, member: discord.Member):
        msg = await ctx.send(f'{ctx.author.mention} has proposed to {member.mention}!\nDo you accept, {member.mention}?')

        def check(emote, user):
            return user == member and str(emote.emoji) in [self.emotes["OK"], self.emotes["ERROR"]]

        try:
            await msg.add_reaction(self.emotes["OK"])
            await msg.add_reaction(self.emotes["ERROR"])
            reaction, message = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
            if message.id == msg.id:
                if str(reaction.emoji) == self.emotes["OK"]:
                    await ctx.send(f'{ctx.author.mention} and {member.mention} are now married!')
                elif str(reaction.emoji) == self.emotes["ERROR"]:
                    await ctx.send(f'{ctx.author.mention} has rejected {member.mention}!')
                else:
                    await ctx.send("oh no")
            

        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond!")
            await msg.remove_reactions()

    @marry.error
    async def marry_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify a user to propose to!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("That user doesn't exist!")
        else:
            await ctx.send("Some error occured.")
            raise error





def setup(client):
    client.add_cog(Wedding(client))