import pytz

from datetime import datetime


def convert_timezone(dt: datetime, tz: str = "Europe/Berlin") -> datetime:
    """Converts a datetime object to the specified timezone — naive -> aware

    Parameters
    ----------
    dt : datetime.datetime
        The datetime object to convert
    tz : str
        The timezone to convert to

    Returns
    -------
    datetime.datetime
        The converted datetime object
    """
    return dt.astimezone(pytz.timezone(tz))
