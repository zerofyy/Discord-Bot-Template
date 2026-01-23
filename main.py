import time

from utils.core import Installer
from utils.assets import CommandArgs
from utils.logging import Logger

try:
    from discord.ext import commands

    from utils.core import Bot
    from utils.assets import Coloring
    # from utils.extension_manager import ExtManager

    _DEPENDENCIES_AVAILABLE = True

    Bot = Bot()
    Coloring.init()

    with open('utils/assets/logo.txt', 'r') as file:
        print(Coloring.gradient(file.read(), start = (114, 137, 218), end = (204, 112, 216)))

except ImportError:
    commands = Bot = Coloring = ExtManager = None

    _DEPENDENCIES_AVAILABLE = False

    with open('utils/assets/logo.txt', 'r') as file:
        print(file.read())


time_start = time.time()
CommandArgs.define()
CommandArgs.parse()
Logger = Logger()


if CommandArgs.logs_file is None:
    Logger.setup()
else:
    Logger.setup(new_file = False)
    Logger.set_file(CommandArgs.logs_file)

if CommandArgs.install:
    Installer.ensure_requirements()

    if not _DEPENDENCIES_AVAILABLE:
        Installer.restart()

elif not _DEPENDENCIES_AVAILABLE:
    Logger.critical('Main', 'One or more modules failed to import, likely due to missing requirements.')
    Logger.info('Main', 'The program cannot continue without installing the necessary modules.')

    if input(' ' * 53 + 'Would you like to run the installer? [y/n] : ').lower().startswith('y'):
        Logger.info('Main', 'User agreed to run the installer.')
        Installer.restart(cmd_args = ['--install', '--logs-file', Logger.get_path('current')])
    else:
        Logger.info('Main', 'User did not agree to run the installer.')
        Logger.info('Main', 'Shutting down...')
        time.sleep(2)
        exit(0)


class DiscordClientHook(commands.Bot):
    async def setup_hook(self) -> None:
        # Load extensions
        # Create init message
        # Log init message
        # Bot is ready
        # Send restart feedback if the bot was restarted
        pass

Bot.setup(DiscordClientHook, prefix = CommandArgs.prefix if CommandArgs.prefix else '>')
Logger.refresh_globals()
client = Bot.client

@client.event  # may not be needed
async def on_ready():
    Logger.ok('Main', 'Hello World!')
    Logger.info('Main', f'Time Taken: {time.time() - time_start:.2f}')


# Run the bot
Logger.info('Main', 'Starting...')
Bot.run()
