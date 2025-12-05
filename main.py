from discord.ext import commands

from utils.core import Bot
from utils.logging import Logger


Logger = Logger()
Bot = Bot()


class CustomClient(commands.Bot):
    async def setup_hook(self) -> None:
        pass


Bot.setup(CustomClient, '>')
Logger.setup()
client = Bot.client


@client.event
async def on_ready():
    Logger.ok('Main', 'Hello World!')


Logger.info('Main', 'Starting...')
Bot.run()
