import datetime


class PlainLogger:
    """ Static class for simple logging. """

    LOG_CODES = {
        '[i]' : 'INFO:',
        '[o]' : '  OK:',
        '[!]' : 'WARN:',
        '[-]' : ' ERR:',
        '[X]' : 'CRIT:',
        '[_]' : '    :'
    }


    @staticmethod
    def _log(code: str, title: str, message: str) -> None:
        """ Helper function for making log entries. """

        time = datetime.datetime.now(tz = None).replace(microsecond = 0)
        header = f'{code} [{time}][{title.center(25)}] {PlainLogger.LOG_CODES.get(code)}'

        lines = message.split('\n')
        entry = f'{header} {lines[0]}'

        spacing = ' ' * len(header)
        for line in lines[1:]:
            entry += f'\n{spacing} {line}'

        print(entry)


    @staticmethod
    def info(title: str, message: str) -> None:
        """
        Make a log entry with an informational message.

        ------

        Arguments:
            title: Title of the log entry, usually the module from which it is logged.
            message: The log message.
        """

        PlainLogger._log('[i]', title, message)


    @staticmethod
    def ok(title: str, message: str) -> None:
        """
        Make a log entry with a message for a successfully finished process.

        ------

        Arguments:
            title: Title of the log entry, usually the module from which it is logged.
            message: The log message.
        """

        PlainLogger._log('[o]', title, message)


    @staticmethod
    def warning(title: str, message: str) -> None:
        """
        Make a log entry with a warning message.

        ------

        Arguments:
            title: Title of the log entry, usually the module from which it is logged.
            message: The log message.
        """

        PlainLogger._log('[!]', title, message)


    @staticmethod
    def error(title: str, message: str) -> None:
        """
        Make a log entry with an error message.

        ------

        Arguments:
            title: Title of the log entry, usually the module from which it is logged.
            message: The log message.
        """

        PlainLogger._log('[-]', title, message)


    @staticmethod
    def critical(title: str, message: str) -> None:
        """
        Make a log entry with a critical error message.

        ------

        Arguments:
            title: Title of the log entry, usually the module from which it is logged.
            message: The log message.
        """

        PlainLogger._log('[X]', title, message)


    @staticmethod
    def log(title: str, message: str) -> None:
        """
        Make a log entry without a specified level.

        ------

        Arguments:
            title: Title of the log entry, usually the module from which it is logged.
            message: The log message.
        """

        PlainLogger._log('[_]', title, message)


__all__ = ['PlainLogger']
