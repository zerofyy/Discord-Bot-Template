import logging
import os
import sys
from pathlib import Path
import asyncio
import datetime


try:
    from utils.core import Bot
    from utils.helpers import Misc
    from utils.assets import Coloring, Emoji, Channels

    import discord

    client = Bot().client
    Text = Coloring.Text

    _DEPENDENCIES_AVAILABLE = True

except ImportError as e:
    Bot = Misc = Coloring = Emoji = Channels = discord = None

    client = None
    Text = None

    _DEPENDENCIES_AVAILABLE = False


class LogLevel:
    """ Log level definitions. """

    def __init__(self, code: str, emoji: str, color_ascii: str, color_hex: int) -> None:
        """
        Create a new LogLevel object.

        ------

        Arguments:
             code: The symbol at the start of each log entry.
             emoji: The emoji used when sending log entries to Discord.
             color_ascii: The ASCII color code for log entries.
             color_hex: The color of embeds when sending log entries to Discord.
        """

        self.code, self.emoji, self.color_ascii, self.color_hex = code, emoji, color_ascii, color_hex


    def unpack(self) -> tuple[str, str, str, int]:
        """ Get the log level information. """

        return self.code, self.emoji, self.color_ascii, self.color_hex


class Logger:
    """ Singleton class for logging. """

    _instance: 'Logger' = None
    _is_setup: bool = False
    file: str = None
    get_current_time: callable = None

    INFO: LogLevel = None
    OK: LogLevel = None
    WARNING: LogLevel = None
    ERROR: LogLevel = None
    CRITICAL: LogLevel = None
    DEFAULT: LogLevel = None


    def __new__(cls) -> 'Logger':
        """ Create an instance of the Logger class or get an already existing instance. """

        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)

        return cls._instance


    def refresh_globals(self) -> None:
        """ Refresh global variables. """

        global client, Text

        if _DEPENDENCIES_AVAILABLE:
            client = Bot().client
            Text = Coloring.Text
            self.ok('Logger', 'Successfully refreshed global variables.')
            return

        self.warning('Logger', 'Failed to refresh global variables due to missing dependencies.')


    def setup(self, new_file: bool = True) -> None:
        """
        Set up the Logger.

        ------

        Arguments:
            new_file: Whether to start a new logs file.
        """

        if self._is_setup:
            self.warning('Logger', 'Logger is already set up.')
            return

        # Set up time function
        def get_current_time(time_format: str = '%d-%m-%Y %H:%M:%S', as_dt: bool = False):
            datetime_now = datetime.datetime.now(tz = None).replace(microsecond = 0)
            return datetime_now if as_dt else datetime_now.strftime(time_format)

        self.get_current_time = Misc.get_current_time if _DEPENDENCIES_AVAILABLE else get_current_time

        # Set up log levels
        if _DEPENDENCIES_AVAILABLE:
            lvl_info = [Emoji.info, Text.li_blue, Coloring.blue]
            lvl_ok = [Emoji.success, Text.li_green, Coloring.green]
            lvl_warning = [Emoji.warning, Text.li_yellow, Coloring.yellow]
            lvl_error = [Emoji.error, Text.li_red, Coloring.red]
            lvl_critical = [Emoji.danger, Text.red, Coloring.pink]
            lvl_default = [Emoji.question, Text.rs, Coloring.white]
        else:
            lvl_info = lvl_ok = lvl_warning = lvl_error = lvl_critical = lvl_default = ['', '', 0]

        self.INFO = LogLevel('[i]', *lvl_info)
        self.OK = LogLevel('[o]', *lvl_ok)
        self.WARNING = LogLevel('[!]', *lvl_warning)
        self.ERROR = LogLevel('[-]', *lvl_error)
        self.CRITICAL = LogLevel('[X]', *lvl_critical)
        self.DEFAULT = LogLevel('[_]', *lvl_default)
        self.ok('Logger', 'Successfully created log levels.')

        # Start a new logs file
        if new_file:
            self.new_file()

        # Log uncaught errors before crashing
        def new_excepthook(exc_type, value, traceback):
            self.critical('Crash Report', f'Type      : {exc_type}\n'
                                          f'Value     : {value}\n'
                                          f'Traceback : {traceback}')
        sys.excepthook = new_excepthook
        self.ok('Logger', 'Successfully configured the system exception hook.')

        # Set up handling for Discord logs
        if _DEPENDENCIES_AVAILABLE:
            handler = LogsHandler()
            handler.setFormatter(logging.Formatter('%(message)s'))

            discord_loggers = [
                'discord',
                'discord.client',
                'discord.gateway',
                'discord.http',
                'discord.state',
                'discord.voice_state',
                'discord.gateway',
                'discord.ext.commands'
            ]

            for disc_logger in discord_loggers:
                disc_logger = logging.getLogger(disc_logger)

                for disc_handler in disc_logger.handlers:
                    disc_logger.removeHandler(disc_handler)

                disc_logger.addHandler(handler)
                disc_logger.setLevel(logging.INFO)
                disc_logger.propagate = False

            self.ok('Logger', 'Successfully configured Discord loggers.')

        else:
            self.info('Logger', 'Skipped Discord loggers configuration.')

        # Set up done
        self._is_setup = True
        self.ok('Logger', 'Finished setting up.')


    def new_file(self) -> None:
        """ Start a new logs file. """

        time = self.get_current_time(time_format = '%d-%m-%Y %H-%M-%S')
        self.file = f'logs/{time}.log'
        self.ok('Logger', 'Successfully started a new logs file.')


    def set_file(self, path: str) -> None:
        """
        Change the current logs file.

        ------

        Arguments:
             path: Path to the new logs file.
        """

        if not Path(path).exists():
            self.error('Logger', f'Failed to change the logs file to "{path}".')
            return

        self.file = path
        self.ok('Logger', f'Successfully changed the logs file to "{path}".')


    def get_level_info(self, level: str) -> tuple[str, str, str, int]:
        """
        Get information for a specific log level.

        ------

        Arguments:
            level: The log level name.

        ------

        Returns:
            The log level's code, emoji, ASCII color code, and hexadecimal color code.
        """

        level = level.lower()
        for name, obj in dict(self.__dict__).items():
            if name.lower() == level and isinstance(obj, LogLevel):
                return obj.unpack()

        return self.DEFAULT.unpack()


    def _log(self, level: str, title: str, message: str, report: bool = False) -> None:
        """ Helper function for making log entries. """

        time = self.get_current_time()
        code, _, color, _ = self.get_level_info(level)

        time_color, title_color = (Text.li_cyan, Text.li_magenta) if _DEPENDENCIES_AVAILABLE else ('', '')

        file_format = f'{code} [{time}][{title.center(25)}]'
        cons_format = f'{color}{code} {time_color}[{time}]{title_color}[{title.center(25)}]'

        lines = message.split('\n')
        file_entry = f'{file_format} {lines[0]}\n'
        cons_entry = f'{cons_format} {color}{lines[0]}'

        spacing = ' ' * len(file_format)
        for line in lines[1:]:
            file_entry += f'\n{spacing} {line}\n'
            cons_entry += f'\n{spacing} {color}{line}'

        print(cons_entry)

        if self.file:
            with open(self.file, 'a', encoding = 'UTF-8') as file:
                file.write(file_entry)

        if report:
            asyncio.run(self._report(level, title, message))


    async def _report(self, level: str, title: str, message: str) -> None:
        """ Helper function for sending log entries to Discord. """

        if not _DEPENDENCIES_AVAILABLE:
            self.error('Logger', 'Unable to report logs to Discord due to missing dependencies.')
            return

        level = level.lower()
        if level in ['warning', 'error', 'critical']:
            channel = client.get_channel(Channels.errors)
        else:
            channel = client.get_channel(Channels.logs)

        _, emoji, _, color = self.get_level_info(level)
        embed = discord.Embed(color = color, description = message, timestamp = self.get_current_time(as_dt = True))
        await channel.send(f'### {emoji} {title}', embed = embed)


    def info(self, title: str, message: str, report: bool = False) -> None:
        """
        Make a log entry with an informational message.

        ------

        Arguments:
            title: Title of the log entry, usually the module from which it is logged.
            message: The log message.
            report: Whether to send the log entry to Discord. Defaults to False.
        """

        self._log('info', title, message, report)


    def ok(self, title: str, message: str, report: bool = False) -> None:
        """
        Make a log entry with a message for a successfully finished process.

        ------

        Arguments:
            title: Title of the log entry, usually the module from which it is logged.
            message: The log message.
            report: Whether to send the log entry to Discord. Defaults to False.
        """

        self._log('ok', title, message, report)


    def warning(self, title: str, message: str, report: bool = False) -> None:
        """
        Make a log entry with a warning message.

        ------

        Arguments:
            title: Title of the log entry, usually the module from which it is logged.
            message: The log message.
            report: Whether to send the log entry to Discord. Defaults to False.
        """

        self._log('warning', title, message, report)


    def error(self, title: str, message: str, report: bool = False) -> None:
        """
        Make a log entry with an error message.

        ------

        Arguments:
            title: Title of the log entry, usually the module from which it is logged.
            message: The log message.
            report: Whether to send the log entry to Discord. Defaults to False.
        """

        self._log('error', title, message, report)


    def critical(self, title: str, message: str, report: bool = False) -> None:
        """
        Make a log entry with a critical error message.

        ------

        Arguments:
            title: Title of the log entry, usually the module from which it is logged.
            message: The log message.
            report: Whether to send the log entry to Discord. Defaults to False.
        """

        self._log('critical', title, message, report)


    def log(self, title: str, message: str, report: bool = False) -> None:
        """
        Make a log entry without a specified level.

        ------

        Arguments:
            title: Title of the log entry, usually the module from which it is logged.
            message: The log message.
            report: Whether to send the log entry to Discord. Defaults to False.
        """

        self._log('', title, message, report)


    def get_path(self, option: str) -> str | None | list[str]:
        """
        Get paths to log files.

        ------

        Options:
            current: The current logs file.

            last: The previous logs file.

            all: All log files.

        ------

        Arguments:
            option: Which log files to retrieve.

        ------

        Returns:
            The paths to the selected log files, or None if no files are found.
        """

        files = list(Path('logs').glob('*.log'))
        if not files:
            return None

        match option.lower():
            case 'current':
                return self.file

            case 'last':
                file = max(files, key = lambda x: x.stat().st_ctime)
                return f'logs/{file.name}'

            case 'all':
                return [f'logs/{file.name}' for file in files]

            case _:
                self.error(
                    'Logger', f'Invalid option "{option}" given for Logger.get_path(option).',
                    report = True
                )


    async def archive(self, path: str) -> None:
        """
        Move a logs file to Discord.

        ------

        Arguments:
             path: The logs file path.
        """

        if not _DEPENDENCIES_AVAILABLE:
            self.error('Logger', 'Unable to archive logs due to missing dependencies.')
            return

        file = Path(path)
        if not file.exists() or not file.is_file():
            self.error('Logger', f'Invalid path "{path}" given for Logger.archive(path).', report = True)
            return

        channel = client.get_channel(Channels.logs)
        await channel.send(f'### {Emoji.upload} Archived: {file.name}', file = discord.File(file))

        if path != self.file:
            os.remove(path)


class LogsHandler(logging.Handler):
    """ Handler subclass for redirecting Discord logs to the custom logger. """

    logger = Logger()


    def emit(self, record: logging.LogRecord) -> None:
        """ Redirect Discord log records to the custom logger. """

        match record.levelno:
            case logging.INFO:
                log_func = self.logger.info

            case logging.WARNING:
                log_func = self.logger.warning

            case logging.ERROR:
                log_func = self.logger.error

            case logging.CRITICAL:
                log_func = self.logger.critical

            case _:
                log_func = self.logger.log

        message = self.format(record)
        log_func(title = record.name, message = message, report = False)



__all__ = ['Logger']
