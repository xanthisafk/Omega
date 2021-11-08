# https://www.youtube.com/watch?v=OGeu_IS0o1A
# This entire code is based on this tutorial. ^^^
# A lot of changes were made to the code so that it would behave like I wanted to.
# I also added a few more things to make it more user friendly.
# Thank you https://github.com/Carberra/discord.py-music-tutorial

import asyncio
import datetime as dt
import enum
import random
import re
import typing as t
from enum import Enum

import aiohttp
import discord
from discord.ext.commands.errors import CommandInvokeError
import wavelink
from discord.ext import commands
from config import EMOTE_ERROR, EMOTE_LEFT,EMOTE_OK, EMOTE_RIGHT,NAME as configname, EMOTE_ZERO,EMOTE_ONE,EMOTE_TWO,EMOTE_THREE,EMOTE_FOUR,EMOTE_FIVE,EMOTE_SIX

rang = [
    0x6100fd, 0xf800b8, 0xff0074, 0xff7343, 0xffbe39, 0xf9f871
]

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
LYRICS_URL = "https://some-random-api.ml/lyrics?title="
HZ_BANDS = (20, 40, 63, 100, 150, 250, 400, 450, 630, 1000, 1600, 2500, 4000, 10000, 16000)
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
OPTIONS = {
    EMOTE_ONE: 0,
    EMOTE_TWO: 1,
    EMOTE_THREE: 2,
    EMOTE_FOUR: 3,
    EMOTE_FIVE: 4,
}


class AlreadyConnectedToChannel(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} Already connected to a channel.")


class NoVoiceChannel(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} No voice channel found.")


class QueueIsEmpty(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} Queue is empty.")


class NoTracksFound(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} No tracks found.")


class PlayerIsAlreadyPaused(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} Player is already paused.")


class NoMoreTracks(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} No more tracks.")


class NoPreviousTracks(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} No previous tracks.")


class InvalidRepeatMode(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} Invalid repeat mode.")


class VolumeTooLow(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} Volume too low.")


class VolumeTooHigh(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} Volume too high.")


class MaxVolume(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} Volume is at maximum.")


class MinVolume(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} Volume is at minimum.")


class NoLyricsFound(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} No lyrics found.")


class InvalidEQPreset(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} Invalid EQ preset.")


class NonExistentEQBand(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} Non-existent EQ band.")


class EQGainOutOfBounds(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} Gain out of bounds.")


class InvalidTimeString(commands.CommandError):
    def __init__(self):
        super().__init__(f"{EMOTE_ERROR} Invalid time string.")


class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None

        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()
        self.eq_levels = [0.] * 15
        self.cog_name = __name__[9:]

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel

        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks, choose=False):
        if not tracks:
            raise NoTracksFound

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            await ctx.send(f"Added {tracks[0].title} to the queue.")
        else:
            if choose == False:
                if (track := tracks[0]) is not None:
                    self.queue.add(track)
                    await ctx.send(f"Added {track.title} to the queue.")
            else:
                if (track := await self.choose_track(ctx, tracks)) is not None:
                    self.queue.add(track)
                    await ctx.send(f"Added {track.title} to the queue.")

        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                str(r.emoji) in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )

        embed = discord.Embed(
            title="Choose a song",
            description=(
                "\n".join(
                    f"**{i+1}.** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"
                    for i, t in enumerate(tracks[:5])
                )
            ),
            colour=random.choice(rang),
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results", icon_url='https://i.ibb.co/CB0KQWM/icons8-search-64.png')
        embed.set_footer(text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=20.0, check=_check)
        except asyncio.TimeoutError:
            embed = discord.Embed(description=f'Playing **`{tracks[0]}`**')
            await msg.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[str(reaction.emoji)]]

    async def start_playback(self):
        await self.play(self.queue.current_track)


    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty: 
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)

class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())
        self.botchannel = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f"Music connected to node: `{node.identifier}`")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()
            embed = discord.Embed(color = random.choice(rang), timestamp=dt.datetime.utcnow())
            embed.set_author(name="Now Playing", icon_url='https://i.ibb.co/2dnLj8b/icons8-play-64.png')
            try:
                embed.add_field(name="Title", value=payload.player.queue.current_track.title)
            except:
                await payload.player.teardown()
                self.botchannel.update({payload.player.guild_id: None})
                return
            embed.add_field(name="Uploader", value=payload.player.queue.current_track.author)
            embed.set_thumbnail(url=payload.player.queue.current_track.thumb)

            position = divmod(payload.player.position, 60000)
            length = divmod(payload.player.queue.current_track.length, 60000)
            embed.add_field(name="Position",value=f"{int(position[0])}:{round(position[1]/1000):02}/{int(length[0])}:{round(length[1]/1000):02}")

            channel = self.bot.get_channel(self.botchannel[payload.player.guild_id])
            await channel.send(embed=embed)

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send(f"{EMOTE_ERROR} Music commands are not available in DMs.")
            return False

        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": "127.0.0.1",
                "port": 2333,
                "rest_uri": "http://127.0.0.1:2333",
                "password": "youshallnotpass",
                "identifier": configname,
                "region": "india",
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.command(name="connect", aliases=["join"])
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        embed = discord.Embed(color=random.choice(rang), timestamp=dt.datetime.utcnow())
        embed.set_author(name="Connection", icon_url='https://i.ibb.co/9tggL7N/icons8-connected-64.png')
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        embed.description = f"Connected to **`{channel.name}`**"
        await ctx.send(embed=embed)
        self.botchannel.update({ctx.guild.id: ctx.channel.id})

    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.send(f"{EMOTE_ERROR} Already connected to a voice channel.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send(f"{EMOTE_ERROR} No suitable voice channel was provided.")
        else: raise exc

    @commands.command(name="disconnect", aliases=["leave", "dc", "clear"])
    async def disconnect_command(self, ctx):
        player = self.get_player(ctx)
        await player.teardown()
        embed = discord.Embed(color=random.choice(rang), timestamp=dt.datetime.utcnow())
        embed.set_author(name="Connection", icon_url='https://i.ibb.co/6Jzs4mF/icons8-disconnected-64.png')
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        embed.description = "Successfully disconnected"
        await ctx.send(embed=embed)
        self.botchannel.update({ctx.guild.id: None})
    
    @disconnect_command.error
    async def disconnect_command_error(self, ctx, exc):
        await ctx.send(f'{EMOTE_ERROR} An unexpected error occured.')
        raise exc
    
    @commands.command(name="resume", aliases=["unpause"])
    async def resume_command(self, ctx):
        player = self.get_player(ctx)
        await player.set_pause(False)
        embed = discord.Embed(color=random.choice(rang), timestamp=dt.datetime.utcnow())
        embed.set_author(name="Player", icon_url='https://i.ibb.co/mcPgy27/icons8-circled-play-64-1.png')
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        embed.description = "Resumed"
        await ctx.send(embed=embed)

    @commands.command(name="play",aliases=['p'])
    async def play_command(self, ctx, *, query: t.Optional[str]):
        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)

        if query is None:
            if player.queue.is_empty:
                raise QueueIsEmpty

            await player.set_pause(False)
            embed = discord.Embed(color=random.choice(rang), timestamp=dt.datetime.utcnow())
            embed.set_author(name="Player", icon_url='https://i.ibb.co/mcPgy27/icons8-circled-play-64-1.png')
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            embed.description = "Resumed"
            await ctx.send(embed=embed)

        else:
            if '--choose' in query:
                query = query.replace('--choose', '')
                choose = True
            else:
                choose = False
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"
            if not player.is_playing and player.queue.is_empty:
                await player.add_tracks(ctx, await self.wavelink.get_tracks(query),choose)
                await ctx.invoke(self.playing_command)
            else:
                await player.add_tracks(ctx, await self.wavelink.get_tracks(query),choose)

        self.botchannel.update({ctx.guild.id: ctx.channel.id})

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send(exc)
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send(exc)
        else:
            await ctx.send(f'{EMOTE_ERROR} An unexpected error occured.')
            raise exc

    @commands.command(name="pause")
    async def pause_command(self, ctx):
        player = self.get_player(ctx)

        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_pause(True)
        embed = discord.Embed(description = "Paused the player",color=random.choice(rang), timestamp=dt.datetime.utcnow())
        embed.set_author(name="Player", icon_url='https://i.ibb.co/Cs5fMSS/icons8-pause-button-64-1.png')
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send(f"{EMOTE_ERROR} Player Already paused.")
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
            raise exc

    @commands.command(name="stop")
    async def stop_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        embed = discord.Embed(description = "Stopped",color=random.choice(rang), timestamp=dt.datetime.utcnow())
        embed.set_author(name="Player", icon_url='https://i.ibb.co/9hbsQWR/icons8-stop-64.png')
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="next", aliases=["skip"])
    async def next_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.upcoming:
            return await ctx.invoke(self.stop_command)
            #raise NoMoreTracks

        await player.stop()

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send(f"{EMOTE_ERROR} Queue is empty.")
        elif isinstance(exc, NoMoreTracks):
            await ctx.send(f"{EMOTE_ERROR} No more tracks in queue")
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occured.")
            raise exc

    @commands.command(name="previous", aliases=["prev","last"])
    async def previous_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.history:
            raise NoPreviousTracks

        player.queue.position -= 2
        await player.stop()

    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send(f"{EMOTE_ERROR} Queue is empty.")
        elif isinstance(exc, NoPreviousTracks):
            await ctx.send(f"{EMOTE_ERROR} There are no previous tracks in the queue.")
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
            raise exc

    @commands.command(name="shuffle")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def shuffle_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.shuffle()
        embed = discord.Embed()
        embed.set_author(name="Player", icon_url="https://i.ibb.co/dbg9XxS/icons8-shuffle-64-1.png")
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        embed.description = "Shuffled the queue."
        await ctx.send(embed=embed)

    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, commands.CommandInvokeError):
            if isinstance(exc, QueueIsEmpty):
                await ctx.send(f"{EMOTE_ERROR} The queue could not be shuffled as it is currently empty.")
            else:
                await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
                raise exc
        elif isinstance(exc, commands.CommandOnCooldown):
            await ctx.send(f"{EMOTE_ERROR} You are on cooldown. Please wait {round(exc.retry_after,1)} seconds.")
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
            raise exc

    @commands.command(name="repeat",aliases=['loop'])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def repeat_command(self, ctx, mode: str=None):
        player = self.get_player(ctx)
        if mode is None:
            current = str(player.queue.repeat_mode).split(".")[1]
            if current == "NONE":
                current = "No repeat"
            elif current == "ONE":
                current = "Repeat current track"
            elif current == "ALL":
                current = "Repeat all tracks"

            embed = discord.Embed(title='Current Mode', description=current, color=(random.choice(rang)))
            embed.add_field(name='New repeat mode', value=f'{EMOTE_ONE}:\tNone\n{EMOTE_TWO}:\tOne\n{EMOTE_THREE}:\tAll', inline=False)
            embed.set_author(name=f'Invoked by {ctx.author.display_name}', icon_url='https://i.ibb.co/Dgd6bTv/icons8-repeat-64.png')
            
            message = await ctx.send(embed=embed)

            await message.add_reaction(EMOTE_ONE)
            await message.add_reaction(EMOTE_TWO)
            await message.add_reaction(EMOTE_THREE)

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in [EMOTE_ONE, EMOTE_TWO, EMOTE_THREE]

            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

                    if str(reaction.emoji) == EMOTE_ONE:
                        player.queue.set_repeat_mode("none")
                        embed.description = 'No repeat'
                        await message.edit(embed=embed)
                        await message.remove_reaction(reaction, user)

                    elif str(reaction.emoji) == EMOTE_TWO:
                        player.queue.set_repeat_mode("1")
                        embed.description = 'Repeat one song'
                        await message.edit(embed=embed)
                        await message.remove_reaction(reaction, user)

                    elif str(reaction.emoji) == EMOTE_THREE:
                        player.queue.set_repeat_mode("all")
                        embed.description = 'Repeat all songs'
                        await message.edit(embed=embed)
                        await message.remove_reaction(reaction, user)

                    else:
                        await message.remove_reaction(reaction, user)

                except asyncio.TimeoutError:
                    await message.clear_reactions()
                    embed.remove_field(0)
                    await message.edit(embed=embed)
                    return await message.edit(content=f"Message timed out.")

        else:
            mode = mode.lower()
            if mode in ['one','single','current']:
                mode = '1'
            if mode not in ("none", "1", "all"):
                raise InvalidRepeatMode

            player.queue.set_repeat_mode(mode)

            if mode == "none":
                mode = "No repeat"
            elif mode == "one":
                mode = "Repeat current track"
            elif mode == "all":
                mode = "Repeat all tracks"

            embed = discord.Embed(title='Updated repeat mode', description=f'Current:\t{mode}', color=(random.choice(rang)))
            embed.set_author(name=f'Invoked by {ctx.author.display_name}', icon_url='https://i.ibb.co/Dgd6bTv/icons8-repeat-64.png')
            return await ctx.send(embed=embed)

    @repeat_command.error
    async def repeat_command_error(self, ctx, exc):
        if isinstance(exc, commands.CommandOnCooldown):
            await ctx.send(f'{EMOTE_ERROR} Command is on cooldown. Try again in {round(exc.retry_after,1)} seconds.')
        elif isinstance(exc, commands.CommandInvokeError):
            if isinstance(exc.original, InvalidRepeatMode):
                return await ctx.send(f"{EMOTE_ERROR} Invalid repeat mode.")
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
            raise exc

    @commands.command(name="queue", aliases=["q", "playlist"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def queue_command(self, ctx, show: t.Optional[int] = 10):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            description=f"Showing up to next {show} tracks",
            colour= random.choice(rang),
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Queue", icon_url="https://i.ibb.co/Stq2xxD/icons8-list-64.png")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Currently playing",
            value=f'**{getattr(player.queue.current_track, "title", "No tracks currently playing.")}**',
            inline=False
        )
        if upcoming := player.queue.upcoming:
            embed.add_field(
                name="Next up",
                value="\n".join(t.title for t in upcoming[:show]),
                inline=False
            )

        msg = await ctx.send(embed=embed)

        if len(upcoming) > 10:
            await msg.add_reaction(EMOTE_LEFT)
            await msg.add_reaction(EMOTE_RIGHT)

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in [EMOTE_LEFT, EMOTE_RIGHT]
            
            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

                    if str(reaction.emoji) == EMOTE_LEFT:
                        show -= 10
                        if show == 0:
                            show += 10
                        
                    elif str(reaction.emoji) == EMOTE_RIGHT:
                        show += 10

                    embed.clear_fields()
                    embed.add_field(
                                    name="Next up",
                                    value="\n".join(t.title for t in upcoming[show-10:show]),
                                    inline=False
                                    )
                    await msg.edit(embed=embed)
                    await msg.remove_reaction(reaction, user)

                except asyncio.TimeoutError:
                    await msg.clear_reactions()
                    return await msg.edit(content=f"Message timed out.")

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send(f"{EMOTE_ERROR} The queue is currently empty.")
        elif isinstance(exc, commands.CommandOnCooldown):
            await ctx.send(f'{EMOTE_ERROR} Command is on cooldown. Try again in {round(exc.retry_after,1)} seconds.')
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
            raise exc


    # Requests -----------------------------------------------------------------

    @commands.group(name="volume", invoke_without_command=True)
    async def volume_group(self, ctx, volume: int = None):
        player = self.get_player(ctx)
        if volume is None:
            embed = discord.Embed(color = random.choice(rang), timestamp=dt.datetime.utcnow())
            embed.set_author(name=f'Volume', icon_url='https://i.ibb.co/6RBLQqK/icons8-speaker-64.png')
            embed.add_field(name='Current volume', value=f'{player.volume}%', inline=False)
            embed.set_footer(text=f'Requested by {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
            embed.add_field(name='Legend', value='🔉:\t**-10**\n🔊:\t**+10**', inline=False)
            msg = await ctx.send(embed=embed)

            await msg.add_reaction('🔉')
            await msg.add_reaction('🔊')

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ['🔉', '🔊']

            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)

                    volume = player.volume

                    if str(reaction.emoji) == '🔉':
                        volume -= 10
                    elif str(reaction.emoji) == '🔊':
                        volume += 10

                    if volume < 0:
                        volume = 0

                    if volume > 150:
                        volume = 150

                    await player.set_volume(volume)
                    embed.clear_fields()
                    embed.add_field(name='Current volume', value=f'{player.volume}%', inline=False)
                    await msg.edit(embed=embed)
                    await msg.remove_reaction(reaction, user)

                except asyncio.TimeoutError:
                    await msg.clear_reactions()
                    embed.clear_fields()
                    await msg.edit(embed=embed, content=f"Message timed out.")

        else:
            
            if volume < 0:
                raise VolumeTooLow

            if volume > 150:
                raise VolumeTooHigh

            await player.set_volume(volume)
            embed = discord.Embed(
                description=f"Volume set to {volume}%",
                colour=random.choice(rang),
                timestamp=dt.datetime.utcnow()
            )
            embed.set_author(name="Volume", icon_url="https://i.ibb.co/6RBLQqK/icons8-speaker-64.png")
            embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @volume_group.error
    async def volume_group_error(self, ctx, exc):
        if isinstance(exc, VolumeTooLow):
            await ctx.send(exc)
        elif isinstance(exc, VolumeTooHigh):
            await ctx.send(exc)
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
            raise exc

    @volume_group.command(name="up")
    async def volume_up_command(self, ctx):
        player = self.get_player(ctx)

        if player.volume == 150:
            raise MaxVolume

        await player.set_volume(value := min(player.volume + 10, 150))
        embed = discord.Embed(
                description=f"Volume set to {value:,}%",
                colour=random.choice(rang),
                timestamp=dt.datetime.utcnow()
            )
        embed.set_author(name="Volume", icon_url="https://i.ibb.co/6RBLQqK/icons8-speaker-64.png")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @volume_up_command.error
    async def volume_up_command_error(self, ctx, exc):
        if isinstance(exc, MaxVolume):
            await ctx.send("The player is already at max volume.")
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
            raise exc

    @volume_group.command(name="down")
    async def volume_down_command(self, ctx):
        player = self.get_player(ctx)

        if player.volume == 0:
            raise MinVolume

        await player.set_volume(value := max(0, player.volume - 10))
        embed = discord.Embed(
                description=f"Volume set to {value:,}%",
                colour=random.choice(rang),
                timestamp=dt.datetime.utcnow()
            )
        embed.set_author(name="Volume", icon_url="https://i.ibb.co/6RBLQqK/icons8-speaker-64.png")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @volume_down_command.error
    async def volume_down_command_error(self, ctx, exc):
        if isinstance(exc, MinVolume):
            await ctx.send(f"{EMOTE_ERROR} The player is already at min volume.")
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
            raise exc

    @commands.command(name="lyrics")
    async def lyrics_command(self, ctx, name: t.Optional[str]):
        player = self.get_player(ctx)
        name = name or player.queue.current_track.title

        async with ctx.typing():
            async with aiohttp.request("GET", LYRICS_URL + name, headers={}) as r:
                if not 200 <= r.status <= 299:
                    raise NoLyricsFound

                data = await r.json()

                if len(data["lyrics"]) > 2000:
                    return await ctx.send(f"<{data['links']['genius']}>")

                embed = discord.Embed(
                    title=data["title"],
                    description=data["lyrics"],
                    colour=random.choice(rang),
                    timestamp=dt.datetime.utcnow(),
                )
                embed.set_thumbnail(url=data["thumbnail"]["genius"])
                embed.set_author(name=data["author"], icon_url='https://i.ibb.co/W66B2xd/icons8-musical-notes-64.png')
                await ctx.send(embed=embed)

    @lyrics_command.error
    async def lyrics_command_error(self, ctx, exc):
        if isinstance(exc, NoLyricsFound):
            await ctx.send(f"{EMOTE_ERROR} No lyrics could be found.")
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
            raise exc

    @commands.command(name="eq")
    async def eq_command(self, ctx, preset: str = None):
        player = self.get_player(ctx)

        if preset is None:
            embed = discord.Embed(
                description=f"Current preset: **{player.eq.name}**",
                colour=random.choice(rang),
                timestamp=dt.datetime.utcnow()
            )
            embed.set_author(name="Equalizer", icon_url="https://i.ibb.co/rwHVm3s/icons8-control-panel-64.png")
            embed.add_field(name="Presets", value=f"{EMOTE_ONE}:\tFlat\n{EMOTE_TWO}:\tBoost\n{EMOTE_THREE}:\tMetal\n{EMOTE_FOUR}:\tPiano", inline=False)
            embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            msg =  await ctx.send(embed=embed)

            await msg.add_reaction(EMOTE_ONE)
            await msg.add_reaction(EMOTE_TWO)
            await msg.add_reaction(EMOTE_THREE)
            await msg.add_reaction(EMOTE_FOUR)

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in [EMOTE_ONE, EMOTE_TWO, EMOTE_THREE, EMOTE_FOUR]

            while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)

                    if str(reaction.emoji) == EMOTE_ONE:
                        preset = "flat"

                    elif str(reaction.emoji) == EMOTE_TWO:
                        preset = "boost"

                    elif str(reaction.emoji) == EMOTE_THREE:
                        preset = "metal"

                    elif str(reaction.emoji) == EMOTE_FOUR:
                        preset = "piano"

                    eq = getattr(wavelink.eqs.Equalizer, preset, None)
                    await player.set_eq(eq())

                    embed.description = f"Current preset: **{player.eq.name}**"

                    await msg.edit(embed=embed)
                    await msg.remove_reaction(reaction.emoji, user)
                
                except asyncio.TimeoutError:
                    embed.clear_fields()
                    await msg.clear_reactions()
                    await msg.edit(embed=embed)
                    await msg.edit(content = "Message timed out.")

        else:

            eq = getattr(wavelink.eqs.Equalizer, preset, None)
            if not eq:
                raise InvalidEQPreset

            await player.set_eq(eq())
            embed = discord.Embed(description=f"Equalizer preset set to **{preset}**", colour=random.choice(rang), timestamp=dt.datetime.utcnow())
            embed.set_author(name="Equalizer", icon_url="https://i.ibb.co/rwHVm3s/icons8-control-panel-64.png")
            embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @eq_command.error
    async def eq_command_error(self, ctx, exc):
        if isinstance(exc, InvalidEQPreset):
            await ctx.send("The EQ preset must be either **`flat`**, **`boost`**, **`metal`**, or **`piano`**.")
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
            raise exc

    @commands.command(name="adveq", aliases=["aeq"])
    async def adveq_command(self, ctx, band: int, gain: float):
        player = self.get_player(ctx)

        if not 1 <= band <= 15 and band not in HZ_BANDS:
            raise NonExistentEQBand

        if band > 15:
            band = HZ_BANDS.index(band) + 1

        if abs(gain) > 10:
            raise EQGainOutOfBounds

        player.eq_levels[band - 1] = gain / 10
        eq = wavelink.eqs.Equalizer(levels=[(i, gain) for i, gain in enumerate(player.eq_levels)])
        await player.set_eq(eq)
        embed = discord.Embed(description=f"Equalizer adjusted:\nband **{band}** set to **{gain}**", colour=random.choice(rang), timestamp=dt.datetime.utcnow())
        embed.set_author(name="Equalizer", icon_url="https://i.ibb.co/rwHVm3s/icons8-control-panel-64.png")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

    @adveq_command.error
    async def adveq_command_error(self, ctx, exc):
        if isinstance(exc, commands.MissingRequiredArgument):
            await ctx.send(f"{EMOTE_ERROR} You must specify a band and gain.")
        elif isinstance(exc, NonExistentEQBand):
            await ctx.send(
                "This is a 15 band equaliser -- the band number should be between 1 and 15, or one of the following "
                "frequencies: " + ", ".join(str(b) for b in HZ_BANDS)
            )
        elif isinstance(exc, EQGainOutOfBounds):
            await ctx.send("The EQ gain for any band should be between 10 dB and -10 dB.")
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
            raise exc

    @commands.command(name="playing", aliases=["np"])
    async def playing_command(self, ctx):
        player = self.get_player(ctx)

        if not player.is_playing:
            raise PlayerIsAlreadyPaused

        embed = discord.Embed(
            colour=random.choice(rang),
            timestamp=dt.datetime.utcnow(),
        )
        embed.set_author(name="Now playing", icon_url="https://i.ibb.co/2dnLj8b/icons8-play-64.png")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Title", value=player.queue.current_track.title)
        embed.add_field(name="Uploader", value=player.queue.current_track.author)
        embed.set_thumbnail(url=player.queue.current_track.thumb)

        position = divmod(player.position, 60000)
        length = divmod(player.queue.current_track.length, 60000)
        embed.add_field(
            name="Position",
            value=f"{int(position[0])}:{round(position[1]/1000):02}/{int(length[0])}:{round(length[1]/1000):02}"
        )

        await ctx.send(embed=embed)

    @playing_command.error
    async def playing_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send(f"{EMOTE_ERROR} There is no track currently playing.")
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
            raise exc

    @commands.command(name="skipto", aliases=["playindex"])
    async def skipto_command(self, ctx, index: int):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        if not 0 <= index <= player.queue.length:
            raise NoMoreTracks

        player.queue.position = index - 2
        await player.stop()
        await ctx.send(f"Playing track in position {index}.")
        await ctx.invoke(self.playing_command)

    @skipto_command.error
    async def skipto_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("There are no tracks in the queue.")
        elif isinstance(exc, NoMoreTracks):
            await ctx.send("That index is out of the bounds of the queue.")
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
            raise exc

    @commands.command(name="restart")
    async def restart_command(self, ctx):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        await player.seek(0)
        await ctx.send("Track restarted.")
        await ctx.invoke(self.playing_command)

    @restart_command.error
    async def restart_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("There are no tracks in the queue.")
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
            raise exc

    @commands.command(name="seek")
    async def seek_command(self, ctx, position: str):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        if not (match := re.match(TIME_REGEX, position)):
            raise InvalidTimeString

        if match.group(3):
            secs = (int(match.group(1)) * 60) + (int(match.group(3)))
        else:
            secs = int(match.group(1))

        await player.seek(secs * 1000)
        await ctx.send("Seeked.")
        await ctx.invoke(self.playing_command)
    
    @seek_command.error
    async def seek_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send(exc)
        elif isinstance(exc, InvalidTimeString):
            await ctx.send(exc)
        else:
            await ctx.send(f"{EMOTE_ERROR} An unknown error occurred.")
            raise exc


def setup(bot):
    bot.add_cog(Music(bot))
