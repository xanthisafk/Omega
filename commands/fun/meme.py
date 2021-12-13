import discord
from discord.ext import commands
import APIs.color as rang
import APIs.get_post as reddit
import codecs
import json


class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]
        with codecs.open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.error_emote = config['emotes']['ERROR']
            self.warning_emote = config['emotes']['WARNING']
            config = None


    @commands.command(name="meme", aliases=["memes"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _meme(self, ctx):
        """
        Sends a random meme from reddit.
        """
        # Get a post from the subreddit
        post = await reddit.get_post("memes")
        # If there is no post, return
        if post is None:
            return await ctx.reply(f"{self.error_emote} Could not find a meme")

        # Create embed and send the post
        embed = discord.Embed(title=post.title, url=post.post_url, color=await rang.get_color())
        embed.set_image(url=post.content)
        embed.set_footer(text=f"By {post.author}")
        await ctx.send(embed=embed)
    
    @_meme.error
    async def meme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"{self.warning_emote} You are on cooldown for {round(error.retry_after,2)} seconds")
        else:
            await ctx.send(f"An error occured")
            raise error

    @commands.command(name="dankmeme", aliases=["dankmemes"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _dankmeme(self, ctx):
        """
        Sends a random meme from reddit.
        """
        # Get a post from the subreddit
        post = await reddit.get_post("dankmemes")
        # If there is no post, return
        if post is None:
            return await ctx.reply(f"{self.error_emote} Could not find a *dank* meme")

        # Create embed and send the post
        embed = discord.Embed(title=post.title, url=post.post_url, color=await rang.get_color())
        embed.set_image(url=post.content)
        embed.set_footer(text=f"By {post.author}")
        await ctx.send(embed=embed)

    @_dankmeme.error
    async def dankmeme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"{self.warning_emote} You are on cooldown for {round(error.retry_after,2)} seconds")
        else:
            await ctx.send(f"{self.error_emote} An error occured")
            raise error

    @commands.command(name="terriblefacebookmeme", aliases=["terriblefacebookmemes"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _terriblefacebookmeme(self, ctx):
        """
        Sends a random meme from reddit.
        """
        # Get a post from the subreddit
        post = await reddit.get_post("terriblefacebookmemes")
        # If there is no post, return
        if post is None:
            return await ctx.reply(f"{self.error_emote} Could not find a *terrible* meme from ~~Facebook~~ Meta")

        # Create embed and send the post
        embed = discord.Embed(title=post.title, url=post.post_url, color=await rang.get_color())
        embed.set_image(url=post.content)
        embed.set_footer(text=f"By {post.author}")
        await ctx.send(embed=embed)
        

    @_terriblefacebookmeme.error
    async def terriblefacebookmeme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"{self.warning_emote} You are on cooldown for {round(error.retry_after,2)} seconds")
        else:
            await ctx.send(f"{self.error_emote} An error occured")
            raise error

    @commands.command(name="prequelmeme", aliases=["prequelmemes"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _prequelmeme(self, ctx):
        """
        Sends a random meme from reddit.
        """
        # Get a post from the subreddit
        post = await reddit.get_post("prequelmemes")
        # If there is no post, return
        if post is None:
            return await ctx.reply(f"{self.error_emote} Jedi stopped me from looking for more memes :|")

        # Create embed and send the post
        embed = discord.Embed(title=post.title, url=post.post_url, color=await rang.get_color())
        embed.set_image(url=post.content)
        embed.set_footer(text=f"By {post.author}")
        await ctx.send(embed=embed)

    @_prequelmeme.error
    async def prequelmeme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"{self.warning_emote} You are on cooldown for {round(error.retry_after,2)} seconds")
        else:
            await ctx.send(f"{self.error_emote} An error occured")
            raise error

    @commands.command(name="antimeme", aliases=["antimemes"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _antimeme(self, ctx):
        """
        Sends a random meme from reddit.
        """
        # Get a post from the subreddit
        post = await reddit.get_post("antimemes")
        # If there is no post, return
        if post is None:
            return await ctx.reply(f"{self.error_emote} Some error, idk")

        # Create embed and send the post
        embed = discord.Embed(title=post.title, url=post.post_url, color=await rang.get_color())
        embed.set_image(url=post.content)
        embed.set_footer(text=f"By {post.author}")
        await ctx.send(embed=embed)

    @_prequelmeme.error
    async def antimeme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"{self.warning_emote} You are on cooldown for {round(error.retry_after,2)} seconds")
        else:
            await ctx.send(f"{self.error_emote} An error occured")
            raise error


    




def setup(bot):
    bot.add_cog(Meme(bot))
