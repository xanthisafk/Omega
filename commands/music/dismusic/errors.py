from nextcord.ext.commands.errors import CheckFailure


class NotConnectedToVoice(CheckFailure):
    """User not connected to any voice channel"""

    def __init__(self):
        super().__init__('You are not connected to any voice channels.')


class PlayerNotConnected(CheckFailure):
    """Player not connected"""

    def __init__(self):
        super().__init__('Bot is not connected to voice channel.')


class MustBeSameChannel(CheckFailure):
    """Player and user not in same channel"""

    def __init__(self):
        super().__init__('Bot is not connected to same channel as you.')
