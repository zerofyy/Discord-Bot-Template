from typing import Optional
from abc import ABC, abstractmethod
import datetime
import sys
import functools

from discord.ext import commands, tasks

from utils.assets import Emoji


class ExtensionRegistry:
    """ Registry for all Extension instances. """

    _extensions: dict[str, 'Extension'] = {}
    _categories: dict[str, list['Extension']] = {}


    @classmethod
    def register_category(cls, name: str) -> None:
        """
        Register a new extension category.

        Arguments:
            name: The name of the category.

        Raises:
            ValueError: If a category with the same name already exists.
        """

        name = name.lower()
        if name in cls._categories:
            raise ValueError(f'Extension category with name "{name}" already exists in the registry.')

        cls._categories[name] = []


    @classmethod
    def register_extension(cls, extension: 'Extension') -> None:
        """
        Register a new extension.

        Arguments:
            extension: An Extension object.

        Raises:
            ValueError: If an extension with the same name or alias already exists.
            KeyError: If the extension's category isn't registered.
        """

        names = [extension.name] + (extension.aliases or [])

        to_register = {}

        for name in names:
            if name in cls._extensions:
                raise ValueError(f'Extension with name or alias "{name}" already exists in the registry.')
            to_register[name] = extension

        cls._extensions.update(to_register)

        if extension.category:
            category = extension.category.lower()
            if category not in cls._categories:
                raise KeyError(f'Extension category with name "{category}" does not exist in the registry.')

            cls._categories[category].append(extension)


    @classmethod
    def get_extension(cls, name: str = None) -> Optional['Extension']:
        """
        Get an extension by its name or alias.

        Arguments:
             name: The name or an alias of the extension.

        Returns:
            The extension object or None if not found.
        """

        return cls._extensions.get(name.lower())


    @classmethod
    def get_extensions(cls, category: str = None, working_only: bool = False) -> list['Extension'] | None:
        """
        Get all extensions registered under the given category.

        Arguments:
             category: The name of the extension category.
             working_only: Whether to only include extensions with status "enabled".

        Returns:
            A list of extension objects or None if not found.
        """

        category = category.lower()
        if category not in cls._categories:
            return None

        extensions = cls._categories[category]
        if not working_only:
            return extensions

        extensions = [ext for ext in extensions if ext.status == 'enabled']
        return extensions or None


    @classmethod
    def get_categories(cls) -> list[str] | None:
        """ Get a list of registered extension categories. """

        return cls._categories.keys() or None


class Extension(ABC):
    """ Abstract decorator for Discord extensions. """

    category: str = None
    status: str = 'unknown'
    status_message: str = 'Extension status **unknown**.'
    function: callable = None


    @abstractmethod
    def __init__(self, name: str, aliases: list[str] = None, description: str = None, reminder: str = None,
                 help_message: str | list[str] = None, authorized_servers: list[int] = None) -> None:
        """
        Create a new Extension object.

        Arguments:
             name: The name of the extension.
             aliases: Alternative names or shortcuts for the extension.
             description: A description of the extension.
             reminder: Reminder notes for the extension.
             help_message: An informational message about how the extension works or is supposed to be used.
                           The message can have multiple fields to improve formatting.
             authorized_servers: IDs of servers in which the extension may be used. Defaults to all server availability.
        """

        self.name = name.lower()
        self.aliases = aliases or []

        if description:
            self.description = description
            self.description_short = description.split('\n')[0].strip()
            self.description_inline = description.replace('\n', ' ').strip()
        else:
            self.description = self.description_short = self.description_inline = None

        self.reminder = reminder
        self.help_message_raw = help_message
        self.authorized_servers = authorized_servers


    @property
    def help_message(self) -> str:
        """ Get the extension's help message, formatted for Discord. """

        ext_type_emoji = Emoji.command if self.__class__.__name__ == 'Command' else Emoji.event
        ext_usage = f' {self.signature}' if getattr(self, 'signature', None) else ''
        help_message = f'{ext_type_emoji}`{self.name}{ext_usage}`'

        if self.description:
            help_message += f'\n> -# {Emoji.question} {self.description_inline}'

        if self.aliases:
            ext_aliases = ', '.join([f'`{alias}`' for alias in self.aliases])
            help_message += f'\n -# {Emoji.label} **Aliases:** {ext_aliases}'

        help_message += '\n'

        if isinstance(self.help_message_raw, str):
            help_message += '\n'.join([f'> -# {line}' for line in self.help_message_raw.split('\n')])
            help_message += '\n'

        elif isinstance(self.help_message_raw, list):
            for field in self.help_message_raw:
                help_message += '\n'.join([f'> -# {line}' for line in field.split('\n')])
                help_message += '\n\n'

        ext_status_emoji = {
            'unknown' : Emoji.ext_status.unknown,
            'registered' : Emoji.ext_status.registered,
            'enabled' : Emoji.ext_status.enabled,
            'disabled' : Emoji.ext_status.disabled,
            'error' : Emoji.ext_status.error
        }
        help_message += f'\n-# {ext_status_emoji[self.status]} {self.status_message}'

        if self.reminder:
            help_message += f'\n> -# {Emoji.avatar} *{self.reminder}*.'

        return help_message


    def set_category(self, name: str) -> None:
        """
        Change the extension's category.

        Arguments:
             name: The name of the extension category.
        """

        self.category = name.lower()


    def set_function(self, func: callable) -> None:
        """
        Change the extension's function.

        Arguments:
             func: The function containing the extension's logic.
        """

        self.function = func


    def set_status(self, status: str, message: str) -> None:
        """
        Change the extension's status.

        Arguments:
             status: The status ("unknown", "registered", "enabled", "disabled", or "error").
             message: The status message.

        Raises:
            ValueError: If the given status is not recognized.
        """

        status = status.lower()
        if status not in ('unknown', 'registered', 'enabled', 'disabled', 'error'):
            raise ValueError(f'Extension status "{status}" not recognized.')

        self.status = status
        self.status_message = message


    def __call__(self, func: callable) -> callable:
        """
        Dynamically registers the given function as a Discord extension.

        Arguments:
             func: The logic behind the extension.

        Returns:
            The same function, unchanged.
        """

        self.set_function(func)
        ExtensionRegistry.register_extension(self)
        self.set_status('registered', 'Extension is **registered**.')
        self._inject_setup(func)
        return func


    @abstractmethod
    def _inject_setup(self, func: callable) -> None:
        """
        Inject a discord.py-compatible setup() function required for loading extensions.

        Arguments:
            func: The logic behind the extension.
        """

        pass


class Command(Extension):
    """ Decorator for command-type Discord extensions. """

    def __init__(self, name: str, aliases: list[str] = None, description: str = None, reminder: str = None,
                 help_message: str | list[str] = None, authorized_servers: list[int] = None, signature: str = None,
                 permissions: list[str] = None, cooldown: int = None, cooldown_type: str = None,
                 prerun_checks: list[callable] = None) -> None:
        """
        Create a new Extension object.

        Arguments:
             name: The name of the extension.
             aliases: Alternative names or shortcuts for the extension.
             description: A description of the extension.
             reminder: Reminder notes for the extension.
             help_message: An informational message about how the extension works or is supposed to be used.
                           The message can have multiple fields to improve formatting.
             authorized_servers: IDs of servers in which the extension may be used. Defaults to all server availability.
             signature: Information about the command's usage and required/optional arguments.
             permissions: Permissions required to use the command.
             cooldown: The command's cooldown period in seconds.
             cooldown_type: The type of cooldown ("personal" or "global").
             prerun_checks: Checks to run before executing the command's logic, raising an error if any check fails.
        """

        super().__init__(name, aliases, description, reminder, help_message, authorized_servers)
        self.signature = signature
        self.permissions = permissions
        self.cooldown = cooldown
        self.cooldown_type = cooldown_type.lower() if cooldown_type else None
        self.prerun_checks = prerun_checks


    def _inject_setup(self, func: callable) -> None:
        @commands.hybrid_command(
            name = self.name, aliases = self.aliases, description = self.description_short, with_app_command = True
        )
        @functools.wraps(func)
        async def _command(ctx: commands.Context, *args, **kwargs) -> None:
            await self.function(ctx, *args, **kwargs)

        module = sys.modules[func.__module__]

        async def setup(client: commands.Bot) -> None:
            client.add_command(_command)

            if not self.prerun_checks:
                return

            for check in self.prerun_checks:
                _command.add_check(check)

        module.setup = setup


class Listener(Extension):
    """ Decorator for listener-type Discord extensions. """

    def __init__(self, name: str, event_name: str, aliases: list[str] = None, description: str = None,
                 reminder: str = None, help_message: str | list[str] = None,
                 authorized_servers: list[int] = None) -> None:
        """
        Create a new Extension object.

        Arguments:
             name: The name of the extension.
             event_name: The name of the event as defined by discord.py.
             aliases: Alternative names or shortcuts for the extension.
             description: A description of the extension.
             reminder: Reminder notes for the extension.
             help_message: An informational message about how the extension works or is supposed to be used.
                           The message can have multiple fields to improve formatting.
             authorized_servers: IDs of servers in which the extension may be used. Defaults to all server availability.
        """

        super().__init__(name, aliases, description, reminder, help_message, authorized_servers)
        self.event_name = event_name.lower()


    def _inject_setup(self, func: callable) -> None:
        async def _listener(*args, **kwargs) -> None:
            await self.function(*args, **kwargs)

        module = sys.modules[func.__module__]

        async def setup(client: commands.Bot) -> None:
            client.add_listener(_listener, self.event_name)

        module.setup = setup


class Task(Extension):
    """ Decorator for task-type Discord extensions. """

    def __init__(self, name: str, aliases: list[str] = None, description: str = None, reminder: str = None,
                 help_message: str | list[str] = None, authorized_servers: list[int] = None, seconds: float = None,
                 minutes: float = None, hours: float = None, count: int = None, reconnect: bool = None,
                 time: datetime.time | list[datetime.time] = None) -> None:
        """
        Create a new Extension object.

        Arguments:
             name: The name of the extension.
             aliases: Alternative names or shortcuts for the extension.
             description: A description of the extension.
             reminder: Reminder notes for the extension.
             help_message: An informational message about how the extension works or is supposed to be used.
                           The message can have multiple fields to improve formatting.
             authorized_servers: IDs of servers in which the extension may be used. Defaults to all server availability.
             seconds: Number of seconds between each execution.
             minutes: Number of minutes between each execution.
             hours: Number of hours between each execution.
             count: Number of total executions.
             reconnect: Whether to restart the extension if any errors occur.
             time: The exact time(s) when to execute the task's logic.
                   Cannot be combined with seconds, minutes, or hours.
        """

        super().__init__(name, aliases, description, reminder, help_message, authorized_servers)
        self.seconds = seconds
        self.minutes = minutes
        self.hours = hours
        self.count = count
        self.reconnect = reconnect
        self.time = time


    def _inject_setup(self, func: callable) -> None:
        kwargs = {
            key : val for key, val in {
                'seconds' : self.seconds,
                'minutes' : self.minutes,
                'hours' : self.hours,
                'count' : self.count,
                'reconnect' : self.reconnect,
                'time' : self.time
            }.items() if val is not None
        }

        @tasks.loop(**kwargs)
        async def _task() -> None:
            await self.function()

        module = sys.modules[func.__module__]

        async def setup(client: commands.Bot) -> None:
            _task.start()

        async def teardown(client: commands.Bot) -> None:
            _task.cancel()

        module.setup = setup
        module.teardown = teardown


__all__ = ['Command', 'Listener', 'Task', 'ExtensionRegistry', 'Extension']
