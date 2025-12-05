import datetime
import zoneinfo
import time


class Misc:
    """ Static class with various miscellaneous functions. """

    @staticmethod
    def get_current_time(seconds_only: bool = False,  as_dt: bool = False, timezone: str = 'auto',
                         time_format: str = '%d-%m-%Y %H:%M:%S',) -> str | float | datetime.datetime:
        """
        Get the current time.

        ------

        Arguments:
             seconds_only: Whether to only return the number of seconds since the Epoch.
             as_dt: Whether to only return a datetime object.
             timezone: A specific timezone ('UTC', 'America/New_York', 'Europe/London', ...).
                       Defaults to the local timezone.
             time_format: A datetime format ('%d/%m/%Y', '%H:%M:%S', ...). Does not apply if as_dt is True.

        ------

        Returns:
            The current time as an object, formatted string, or in seconds only.
        """

        if seconds_only:
            return time.time()

        timezone = None if timezone == 'auto' else zoneinfo.ZoneInfo(timezone)
        datetime_now = datetime.datetime.now(tz = timezone).replace(microsecond = 0)

        if as_dt:
            return datetime_now

        return datetime_now.strftime(time_format)


__all__ = ['Misc']
