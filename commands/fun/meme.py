import nextcord
from nextcord.ext import commands
import APIs.color as rang
import loggers.logger as log
import APIs.get_post as reddit
import config


class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]


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
            return await ctx.reply(f"{config.EMOTE_ERROR} Could not find a meme")

        # Create embed and send the post
        embed = nextcord.Embed(title=post.title, url=post.post_url, color=await rang.get_color())
        embed.set_image(url=post.content)
        embed.set_footer(text=f"By {post.author}")
        await ctx.send(embed=embed)
        return await log.logger(ctx, "meme", self.cog_name,"INFO")
    
    @_meme.error
    async def meme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"{config.EMOTE_WARNING} You are on cooldown for {round(error.retry_after,1)} seconds")
        else:
            await ctx.send(f"An error occured")
            log.logger(ctx, "meme", self.cog_name, "ERROR")

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
            return await ctx.reply(f"{config.EMOTE_ERROR} Could not find a *dank* meme")

        # Create embed and send the post
        embed = nextcord.Embed(title=post.title, url=post.post_url, color=await rang.get_color())
        embed.set_image(url=post.content)
        embed.set_footer(text=f"By {post.author}")
        await ctx.send(embed=embed)
        return await log.logger(ctx, "dankmeme", self.cog_name,"INFO")

    @_dankmeme.error
    async def dankmeme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"{config.EMOTE_WARNING} You are on cooldown for {round(error.retry_after,1)} seconds")
        else:
            await ctx.send(f"{config.EMOTE_ERROR} An error occured")
            log.logger(ctx, "dankmeme", self.cog_name, "ERROR")

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
            return await ctx.reply(f"{config.EMOTE_ERROR} Could not find a *terrible* meme from ~~Facebook~~ Meta")

        # Create embed and send the post
        embed = nextcord.Embed(title=post.title, url=post.post_url, color=await rang.get_color())
        embed.set_image(url=post.content)
        embed.set_footer(text=f"By {post.author}")
        await ctx.send(embed=embed)
        return await log.logger(ctx, "terriblefacebookmeme", self.cog_name,"INFO")

    @_terriblefacebookmeme.error
    async def terriblefacebookmeme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"{config.EMOTE_WARNING} You are on cooldown for {round(error.retry_after,1)} seconds")
        else:
            await ctx.send(f"{config.EMOTE_ERROR} An error occured")
            log.logger(ctx, "terriblefacebookmeme", self.cog_name, "ERROR")

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
            return await ctx.reply(f"{config.EMOTE_ERROR} Jedi stopped me from looking for more memes :|")

        # Create embed and send the post
        embed = nextcord.Embed(title=post.title, url=post.post_url, color=await rang.get_color())
        embed.set_image(url=post.content)
        embed.set_footer(text=f"By {post.author}")
        await ctx.send(embed=embed)
        return await log.logger(ctx, "prequelmeme", self.cog_name,"INFO")

    @_prequelmeme.error
    async def prequelmeme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"{config.EMOTE_WARNING} You are on cooldown for {round(error.retry_after,1)} seconds")
        else:
            await ctx.send(f"{config.EMOTE_ERROR} An error occured")
            log.logger(ctx, "prequelmeme", self.cog_name, "ERROR")







def setup(bot):
    bot.add_cog(Meme(bot))
