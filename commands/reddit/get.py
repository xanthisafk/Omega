# This is the first cog that was written using Github copilot and so it has a lot of comments.
# I am surprised that it works so well.
# Wow.
import discord
from discord.ext import commands
import APIs.color as rang
import loggers.logger as log
import redditeasy
import random
from datetime import datetime
from asyncio import TimeoutError

class Get(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = __name__[9:]
        self.REDDIT_ID = self.bot.config['reddit']["ID"]
        self.REDDIT_SECRET = self.bot.config['reddit']['SECRET']
        self.EMOTE_UPVOTE = self.bot.config['emotes']['UPVOTE']
        self.EMOTE_LEFT = self.bot.config['emotes']['LEFT']
        self.EMOTE_RIGHT = self.bot.config['emotes']['RIGHT']
        self.EMOTE_ERROR = self.bot.config['emotes']['ERROR']


    @commands.command()
    #@commands.cooldown(1, 10, commands.BucketType.user)
    async def get(self, ctx, sub=''):
        """
        Gets a random post from a subreddit.
        """
        name = "get"
        if sub == '' or sub in ['--controversial', '--hot', '--new','--top']:
            sub += random.choice(['cats', 'rarepuppers', 'memes', 'pics', 'gifs', 'aww', 'gaming', 'funny', 'movies', 'music', 'science', 'sports', 'television'])
        # Create object
        if self.REDDIT_ID == 'None' or self.REDDIT_SECRET == 'None':
            rd = redditeasy.AsyncSubreddit()
        else:
            rd = redditeasy.AsyncSubreddit(client_id=self.REDDIT_ID, client_secret=self.REDDIT_SECRET, user_agent = 'https://github.com/xanthisafk/omega')

        # Get post and loop until image is found
        # If no image is found, return error
        i = 5
        while i > 0:
            try:
                if '--new' in sub:
                    sub = sub.replace('--new', '')
                    post = await rd.get_new_post(subreddit=sub)
                    if post.content_type in ['Image', "Text"]:
                        break
                elif '--hot' in sub:
                    sub = sub.replace('--hot', '')
                    post = await rd.get_hot_post(subreddit=sub)
                    if post.content_type in ['Image', "Text"]:
                        break
                elif '--top' in sub:
                    sub = sub.replace('--top', '')
                    post = await rd.get_top_post(subreddit=sub)
                    if post.content_type in ['Image', "Text"]:
                        break
                elif '--controversial' in sub:
                    sub = sub.replace('--controversial', '')
                    post = await rd.get_controversial_post(subreddit=sub)
                    if post.content_type in ['Image', "Text"]:
                        break
                else:
                    post = await rd.get_post(subreddit=sub)
                    if post.content_type in ['Image', "Text"]:
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
        embed = discord.Embed(title=(post.title[:250]+"..."), description=f'{self.EMOTE_UPVOTE}{post.score}', url=post.post_url, color=await rang.get_color())
        
        embed.timestamp = datetime.fromtimestamp(post.created_at)
        embed.set_footer(text=f'By {post.author} on r/{sub}')
        if post.content_type == 'Image':
            embed.set_image(url=post.content)
        elif post.content_type == 'Text':
            if len(post.content) > 1000:
                embed.add_field(name="Content:",value=(post.content[:1000] + '    **contd.**'))
            else:
                embed.add_field(name="Content:",value=post.content)
        message = await ctx.send(embed=embed)

        if len(post.content) < 1000:
            return
        else:

            await message.add_reaction(self.EMOTE_LEFT)
            await message.add_reaction(self.EMOTE_RIGHT)
            await message.add_reaction(self.EMOTE_ERROR)
            embed.add_field(name="Usage",value=f"{self.EMOTE_LEFT}: Previous  {self.EMOTE_RIGHT}: Next  {self.EMOTE_ERROR}: Close",inline=False)
            embed.set_author(name=f"{ctx.author}",icon_url=ctx.author.avatar_url)
            await message.edit(embed=embed)

            page = 1
            mp = 1
            content = []
            n = 1000
            for i in range(0,len(post.content),n):
                content.append(post.content[i:i+n])
            
            total = len(content)
            for i in range(0,total-1):
                content[i] = content[i] + "    **contd.**"

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in [self.EMOTE_LEFT, self.EMOTE_RIGHT, self.EMOTE_ERROR]

            while True:

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)

                    if str(reaction.emoji) == self.EMOTE_RIGHT and page != total:
                        page += 1
                    elif str(reaction.emoji) == self.EMOTE_LEFT and page > 1:
                        page -= 1
                    elif str(reaction.emoji) == self.EMOTE_ERROR:
                        embed.remove_field(1)
                        await message.edit(embed=embed)
                        await message.clear_reactions()
                        break

                    embed.set_field_at(0, name="Content:", value=content[page-1])

                    await message.remove_reaction(reaction.emoji, user)
                    await message.edit(embed=embed)

                except TimeoutError:
                    await message.clear_reactions()
                    embed.remove_field(1)
                    await message.edit(content="Message timed out", embed=embed)
                    break




    @get.error
    async def get_error(self, ctx, error):
        # Error handling for cooldown
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.reply(f'Slow down! Cooldown ends in: {round(error.retry_after,2)}s')
        elif isinstance(error, redditeasy.exceptions.RequestError):
            return await ctx.reply(f'Error: {error.with_traceback}')
        elif isinstance(error,redditeasy.exceptions.EmptyResult):
            return await ctx.reply(f"{self.EMOTE_ERROR} Results came back empty!")
        else:
            await ctx.send(f'{self.EMOTE_ERROR} An unexpected error occured')
            raise error



def setup(bot):
    bot.add_cog(Get(bot))
