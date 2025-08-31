#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zoneinfo

from datetime import datetime
from datetime import timezone as datetime_timezone

from core.config import settings


class TimeZone:
    def __init__(self, tz: str = settings.DATETIME_TIMEZONE) -> None:
        """
        Initialize the timezone converter.

        :param tz: Timezone name. Defaults to settings.DATETIME_TIMEZONE.
        """
        self.tz_info = zoneinfo.ZoneInfo(tz)

    def now(self) -> datetime:
        """Get the current time in the configured timezone."""
        return datetime.now(self.tz_info)

    def f_datetime(self, dt: datetime) -> datetime:
        """
        Convert a datetime object to the configured timezone.

        :param dt: The datetime object to convert.
        :return: The datetime adjusted to the configured timezone.
        """
        return dt.astimezone(self.tz_info)

    def f_str(self, date_str: str, format_str: str = settings.DATETIME_FORMAT) -> datetime:
        """
        Parse a time string into a datetime object in the configured timezone.

        :param date_str: The time string to parse.
        :param format_str: Format string for parsing. Defaults to settings.DATETIME_FORMAT.
        :return: The parsed datetime object with timezone info.
        """
        return datetime.strptime(date_str, format_str).replace(tzinfo=self.tz_info)

    @staticmethod
    def t_str(dt: datetime, format_str: str = settings.DATETIME_FORMAT) -> str:
        """
        Format a datetime object into a string using the specified format.

        :param dt: The datetime object to format.
        :param format_str: Format string for output. Defaults to settings.DATETIME_FORMAT.
        :return: Formatted datetime string.
        """
        return dt.strftime(format_str)

    @staticmethod
    def f_utc(dt: datetime) -> datetime:
        """
        Convert a datetime object to UTC timezone.

        :param dt: The datetime object to convert.
        :return: The datetime adjusted to UTC timezone.
        """
        return dt.astimezone(datetime_timezone.utc)


timezone: TimeZone = TimeZone()