# This is the first cog that was written using Github copilot and so it has a lot of comments.
# I am surprised that it works so well.
# Wow.
import discord
from discord.ext import commands
import APIs.color as rang
import loggers.logger as log
import redditeasy
import config
import random
from datetime import datetime

class Get(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def get(self, ctx, sub=''):
        """
        Gets a random post from a subreddit.
        """
        name = "get"
        if sub == '' or sub in ['--controversial', '--hot', '--new','--top']:
            sub += random.choice(['cats', 'rarepuppers', 'memes', 'pics', 'gifs', 'aww', 'gaming', 'funny', 'movies', 'music', 'science', 'sports', 'television'])
        # Create object
        if config.REDDIT_CLIENT_ID == 'None' or config.REDDIT_CLIENT_SECRET == 'None':
            rd = redditeasy.AsyncSubreddit()
        else:
            rd = redditeasy.AsyncSubreddit(client_id=config.REDDIT_CLIENT_ID, client_secret=config.REDDIT_CLIENT_SECRET, user_agent = 'https://github.com/xanthisafk/omega')

        # Get post and loop until image is found
        # If no image is found, return error
        i = 5
        while i > 0:
            try:
                if '--new' in sub:
                    sub = sub.replace('--new', '')
                    post = await rd.get_new_post(subreddit=sub)
                    if post.content_type == 'Image':
                        break
                elif '--hot' in sub:
                    sub = sub.replace('--hot', '')
                    post = await rd.get_hot_post(subreddit=sub)
                    if post.content_type == 'Image':
                        break
                elif '--top' in sub:
                    sub = sub.replace('--top', '')
                    post = await rd.get_top_post(subreddit=sub)
                    if post.content_type == 'Image':
                        break
                elif '--controversial' in sub:
                    sub = sub.replace('--controversial', '')
                    post = await rd.get_controversial_post(subreddit=sub)
                    if post.content_type == 'Image':
                        break
                else:
                    post = await rd.get_post(subreddit=sub)
                    if post.content_type == 'Image':
                        break
                i -= 1
            except Exception as e:
                if isinstance(e,ValueError):
                    return await ctx.reply(f'Invalid subreddit name `{sub}`')
        else:
            return await ctx.reply(f"No image found in {sub}")

        # If the post is nsfw, check if the channel is nsfw
        if post.nsfw:
            if not ctx.channel.is_nsfw():
                return await ctx.send(random.choice(['Bonk','bonk!','bonk','Bonk!','🙄😶','🙈']))

        # Create embed and send
        embed = discord.Embed(title=post.title, description=f'{config.EMOTE_UPVOTE}{post.score}', url=post.post_url, color=await rang.get_color())
        embed.set_image(url=post.content)
        embed.timestamp = datetime.fromtimestamp(post.created_at)
        embed.set_footer(text=f'By {post.author} on r/{sub}')
        return await ctx.send(embed=embed)

    @get.error
    async def get_error(self, ctx, error):
        # Error handling for cooldown
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.reply(f'Slow down! Cooldown ends in: {round(error.retry_after,1)}s')
        elif isinstance(error, redditeasy.exceptions.RequestError):
            return await ctx.reply(f'Error: {error.with_traceback}')
        elif isinstance(error,redditeasy.exceptions.EmptyResult):
            return await ctx.reply(f"{config.EMOTE_ERROR} Results came back empty!")
        else:
            await ctx.send(f'{config.EMOTE_ERROR} An unexpected error occured')
            raise error



def setup(bot):
    bot.add_cog(Get(bot))
