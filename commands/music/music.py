import discord, random
from discord.ext import commands

import youtube_dl


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue_ = {}

    @commands.command(aliases=['connect'])
    @commands.guild_only()
    async def join(self, ctx, *, a=''):

        channel = ctx.message.author.voice.channel
        try:
            await channel.connect()
            await ctx.send(f'Joined `{channel.name}`.')
        except Exception as e:
            if '--forced' in a or '--f' in a:
                pass
            else:
                await ctx.send(e)

        voice = ctx.guild.voice_client
        a.lower()
        if '--forced' in a or '--f' in a:
            await voice.move_to(ctx.author.voice.channel)
            await ctx.send(f'Moved to `{ctx.author.voice.channel}`')
 
    
    @commands.command(aliases=['p'])
    async def play(self,ctx,url:str):

        voice_channel = ctx.message.author.voice.channel
        voice = ctx.guild.voice_client
        if voice == None:
            await voice_channel.connect()
            voice = ctx.guild.voice_client

        if voice.is_playing():
            await self._queue(ctx,url)
            return

        ytdl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet':True
        }

        with youtube_dl.YoutubeDL(ytdl_opts) as yt:
             song_info = yt.extract_info(url, download=False)
        voice.play(discord.FFmpegPCMAudio(song_info["formats"][0]["url"]))
        await ctx.send(f'Now playing: {song_info["title"]}')
    
    @commands.command(aliases=['disconnect'])
    async def leave(self, ctx,*,a=' '):
        voice = ctx.guild.voice_client
        if voice == None:
            await ctx.send(('?'*(random.randint(1,10))))
            return
        if voice.is_connected() and voice.channel ==  ctx.message.author.voice.channel:
            await voice.disconnect()
            await ctx.send(f'Left `{voice.channel}`.')
        elif ['--f', '--force'] in a:
            await voice.disconnect()
            await ctx.send(f'Left `{voice.channel}`')
        else:
            await ctx.send(f"{('?'*(random.randint(1,10)))}\nI am currently connected to `{voice.channel}`")

    @commands.command()
    async def pause(self, ctx):
        voice = ctx.guild.voice_client
        
        if voice.is_playing():
            voice.pause()
            await ctx.message.add_reaction('<:ok:899558562819358720>')
        else:
            await ctx.send('Currently not playing anything.')
    
    @commands.command(aliases=["unpause"])
    async def resume(self, ctx):
        voice = ctx.guild.voice_client
        if voice == None:
            await ctx.send('I am not connected anywhere.')
            return
        if voice.is_paused():
            voice.resume()
            await ctx.message.add_reaction('<:ok:899558562819358720>')
        else:
            await ctx.send('Audio is not paused.')
    
    @commands.command()
    async def stop(self, ctx):
        voice = ctx.guild.voice_client
        if voice == None:
            await ctx.send('I am not connected anywhere.')
            return
        if voice.is_playing():
            voice.stop()
            await ctx.message.add_reaction('<:ok:899558562819358720>')
        else:
            await ctx.send("Audio is not playing.")

    async def _queue(self,ctx,url):
        gid = ctx.guild.id
        user = ctx.author
        temp = []
        l = f'{url} ^-^ {user}'
        temp.append(l)
        self.queue_[gid] = temp

    @commands.command()
    async def queue(self, ctx):

        embed = discord.Embed(title=f"Queue for {ctx.guild}")

        ytdl_opts = {'quiet':True}
        gid = ctx.guild.id

        for i in self.queue_[gid]:
            i = i.split('^-^')
            url = i[0]
            user = i[1]
            with youtube_dl.YoutubeDL(ytdl_opts) as yt:
                song_info = yt.extract_info(url, download=False)

                value = f'{song_info["title"]} - Requested by {user}'
                embed.add_field(name=f'Connected to {ctx.guild.voice_client.channel}', value=value, inline=False)
                await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Music(bot))

