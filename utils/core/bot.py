import discord
from discord.ext import commands

import os
import dotenv


class Bot:
    """ Singleton wrapper for the Discord client. """

    _instance: 'Bot' = None
    prefix: str = None
    client: commands.Bot = None


    def __new__(cls) -> 'Bot':
        """ Create an instance of the Bot class or get an already existing instance. """
        
        if cls._instance is None:
            cls._instance = super(Bot, cls).__new__(cls)

        return cls._instance


    def setup(self, hook: type[commands.Bot], prefix: str, intents: discord.Intents = discord.Intents.none(),
              mentions: discord.AllowedMentions = discord.AllowedMentions.none()) -> None:
        """
        Set up the Discord client.

        ------

        Arguments:
            hook: A commands.Bot subclass with a custom setup_hook function.
            prefix: The bot's command prefix.
            intents: The bot's intents. Defaults to all intents disabled.
            mentions: The bot's allowed mentions. Defaults to all mentions disabled.
        """

        if self.client is not None:
            raise RuntimeError('The bot is already set up.')

        self.prefix = prefix
        self.client = hook(
            command_prefix = prefix,
            intents = intents,
            allowed_mentions = mentions,
            case_insensitive = True
        )


    def run(self, token: str = None) -> None:
        """
        Run the Discord client.

        ------

        Arguments:
            token: The Discord client token. Defaults to loading it from the "BOT_TOKEN" environment variable.
        """

        if self.client is None:
            raise RuntimeError('The bot must be set up before running.')

        if token is None:
            dotenv.load_dotenv()
            token = os.getenv('BOT_TOKEN')

            if not token:
                raise ValueError('BOT_TOKEN not found in environment variables.')

        self.client.run(token)


__all__ = ['Bot']
