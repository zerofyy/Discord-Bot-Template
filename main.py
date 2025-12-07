import time

from utils.core import Installer
from utils.assets import CommandArgs


time_start = time.time()


# Parse command-line arguments
CommandArgs.define()
CommandArgs.parse()


# Install requirements
if CommandArgs.install:
    Installer.ensure_requirements()


from discord.ext import commands

from utils.core import Bot
from utils.logging import Logger
from utils.assets import Coloring
# from utils.extension_manager import ExtManager


# Initialization
Coloring.init()
with open('utils/assets/logo.txt', 'r') as file:
    print(Coloring.gradient(file.read(), start = (114, 137, 218), end = (204, 112, 216)))

Bot = Bot()
Logger = Logger()
Logger.setup()


# Create Discord client setup hook
class DiscordClientHook(commands.Bot):
    async def setup_hook(self) -> None:
        # Load extensions
        # Create init message
        # Log init message
        # Bot is ready
        # Send restart feedback if the bot was restarted
        pass

Bot.setup(DiscordClientHook, prefix = CommandArgs.prefix if CommandArgs.prefix else '>')
client = Bot.client

@client.event  # may not be needed
async def on_ready():
    Logger.ok('Main', 'Hello World!')
    Logger.info('Main', f'Time Taken: {time.time() - time_start:.2f}')


# Run the bot
Logger.info('Main', 'Starting...')
Bot.run()
