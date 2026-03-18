import discord
from discord.ext import commands

import os
import dotenv


class Bot:
    """ Static wrapper for the Discord client. """

    prefix: str = None
    client: commands.Bot = None


    @classmethod
    def setup(cls, hook: type[commands.Bot], prefix: str, intents: discord.Intents = discord.Intents.none(),
              mentions: discord.AllowedMentions = discord.AllowedMentions.none()) -> None:
        """
        Set up the Discord client.

        Arguments:
            hook: A commands.Bot subclass with a custom setup_hook function.
            prefix: The bot's command prefix.
            intents: The bot's intents. Defaults to all intents disabled.
            mentions: The bot's allowed mentions. Defaults to all mentions disabled.

        Raises:
            RuntimeError: If the bot is already set up.
        """

        if cls.client is not None:
            raise RuntimeError('The bot is already set up.')

        cls.prefix = prefix
        cls.client = hook(
            command_prefix = prefix,
            intents = intents,
            allowed_mentions = mentions,
            case_insensitive = True
        )


    @classmethod
    def run(cls, token: str = None) -> None:
        """
        Run the Discord client.

        Arguments:
            token: The Discord client token. Defaults to loading it from the "BOT_TOKEN" environment variable.

        Raises:
            RuntimeError: If the bot isn't set up.
            ValueError: If "BOT_TOKEN" is missing from the environment variables.
        """

        if cls.client is None:
            raise RuntimeError('The bot must be set up before running.')

        if token is None:
            dotenv.load_dotenv()
            token = os.getenv('BOT_TOKEN')

            if not token:
                raise ValueError('BOT_TOKEN not found in environment variables.')

        cls.client.run(token)


__all__ = ['Bot']
