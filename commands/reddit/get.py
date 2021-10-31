# This is the first cog that was written using Github copilot and so it has a lot of comments.
# I am surprised that it works so well.
# Wow.
import nextcord
from nextcord.ext import commands
import APIs.color as rang
import loggers.logger as log
import redditeasy
import config
import random

class Get(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def get(self, ctx, sub='all'):
        """
        Gets a random post from a subreddit.
        """
        name = "get"

        # Create object
        rd = redditeasy.AsyncSubreddit()

        # Get post and loop until image is found
        # If no image is found, return error
        i = 5
        while i > 0:
            try:
                post = await rd.get_post(subreddit=sub)
                if post.content_type == 'Image':
                    break
                else:
                    i -= 1
            except Exception as e:
                if isinstance(e,ValueError):
                    return await ctx.reply(f'Invalid subreddit name `{sub}`')
        else:
            return await ctx.reply(f"No image found in {sub}")

        # If the post is nsfw, check if the channel is nsfw
        if post.nsfw:
            if not ctx.channel.is_nsfw():
                return await ctx.send(random.choice(['Bonk','bonk!','bonk','Bonk!','🙄😶']))

        # Create embed and send
        embed = nextcord.Embed(title=post.title, description=f'{config.EMOTE_UPVOTE}{post.score} | {config.EMOTE_DOWNVOTE}{post.downvotes}', url=post.post_url, color=await rang.get_color())
        embed.set_image(url=post.content)
        embed.set_footer(text=f'By {post.author} on r/{sub}')
        await ctx.send(embed=embed)
        return await log.logger(ctx, name, self.cog_name,'INFO')

    @get.error
    async def get_error(self, ctx, error):
        # Error handling for cooldown
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.reply(f'Slow down! Cooldown ends in: {round(error.retry_after,1)}s')
        # Else, log error
        else:
            return await log.logger(ctx, 'get', self.cog_name, 'ERROR', error)



def setup(bot):
    bot.add_cog(Get(bot))
