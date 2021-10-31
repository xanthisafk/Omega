from discord.ext import commands
from .player import DisPlayer
from .errors import NotConnectedToVoice, PlayerNotConnected, MustBeSameChannel

def voice_connected():
    def predicate(ctx):
        try:
            channel = ctx.author.voice.channel
            return True
        except AttributeError:
            raise NotConnectedToVoice()

    return commands.check(predicate)


def player_connected():
    def predicate(ctx):
        player: DisPlayer = ctx.bot.wavelink.get_player(ctx.guild.id, cls=DisPlayer)

        if not player.is_connected:
            raise PlayerNotConnected()
        return True

    return commands.check(predicate)


def in_same_channel():
    def predicate(ctx):
        player: DisPlayer = ctx.bot.wavelink.get_player(ctx.guild.id, cls=DisPlayer)

        if not player.is_connected:
            raise PlayerNotConnected()

        if player.channel_id == ctx.author.voice.channel.id:
            return True
        else:
            raise MustBeSameChannel()

    return commands.check(predicate)
