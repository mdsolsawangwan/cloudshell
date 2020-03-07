#!/usr/bin/env python

import datetime

__all__ = [
    'EPOCH',
    'now',
    'iso_8601',
    'utc_to_local',
    'utc_to_local_str',
    'local_to_utc',
    'local_to_utc_str',
    'seconds_since_epoch',
    'convert_iso_8601_str_to_datetime',
]

EPOCH = datetime.datetime(1970, 1, 1, 0, 0, 0)
LOCAL_FORMAT = '%Y-%m-%d %H:%M:%S.%f %Z%z'
ISO_8601_FORMAT = '%Y-%m-%dT%H:%M:%S%Z'

def now(utc: bool = False) -> datetime.datetime:
    """
    helper method, get the `datetime`, now. defaults to local time.
    """

    return datetime.datetime.utcnow() if utc else datetime.datetime.now()

def seconds_since_epoch(from_t: datetime.datetime = None) -> float:
    """
    if specified, `from_t` must be UTC ISO-8601.
    """

    return (
        (from_t if from_t else now(utc=True)) - EPOCH
    ).total_seconds()

def iso_8601(d: int, m: int, y: int, hour: int = 23, minute: int = 0) -> str:
    """
    returns a date string in the format expected by all aws services. `hour` and `minute`
    are set to default values if out of bounds while `d`ay, `m`onth
    and `y`ear raise `ValueError`.

    >>> iso_8601(19, 3, 2020)
    '2020-03-19T23:00:00Z'
    >>> iso_8601(19, 3, 2020, hour=6)
    '2020-03-19T06:00:00Z'
    >>> iso_8601(19, 3, 2020, hour=65)
    '2020-03-19T00:00:00Z'
    """

    if hour < 0 or hour > 23:
        hour = 23

    if minute < 0 or minute > 59:
        minute = 0

    if y < 1:
        raise ValueError('(y)ear must be in 0..N')

    if m < 1 or m > 12:
        raise ValueError('(m)onth must be in 1..12')

    if d < 1 or d > 31:
        raise ValueError('(d)ay must be in 1..31')

    return datetime.datetime(y, m, d, hour=hour, minute=minute).isoformat() + 'Z'

def convert_iso_8601_str_to_datetime(t: str) -> datetime.datetime:
    """
    convert a date string in aws ISO 8601 format to a `datetime` object.
    """

    return datetime.datetime.strptime(t, ISO_8601_FORMAT)

def utc_to_local(t: datetime.datetime) -> datetime.datetime:
    """
    convert a UTC `datetime` object to a local `datetime`.
    """

    return t.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)

def utc_to_local_str(t: datetime.datetime) -> str:
    """
    convert a UTC `datetime` object to a local date string.
    """

    return utc_to_local(t).strftime(LOCAL_FORMAT)

def local_to_utc(t: datetime.datetime) -> datetime.datetime:
    """
    convert to a local `datetime` object to a UTC `datetime`.
    """

    return t.replace(tzinfo=None).astimezone(tz=datetime.timezone.utc)

def local_to_utc_str(t: datetime.datetime) -> str:
    """
    convert to a local `datetime` object to a UTC date string.
    """

    return local_to_utc(t).strftime(ISO_8601_FORMAT)

# import time
# import calendar

# def local_to_utc(t: str) -> time.struct_time:
#     """
#     >>> local_to_utc('2000-03-12 02:00')
#     time.struct_time(tm_year=2020, tm_mon=3, tm_mday=19, tm_hour=7, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=79, tm_isdst=0)
#     """

#     time_tuple = time.strptime(t, '%Y-%m-%d %I:%M')
#     secs = time.mktime(time_tuple) # DST flag must be -1. this tells mktime to take daylight savings into account
#     return time.gmtime(secs)

# def utc_to_local(t: str) -> time.struct_time:
#     """
#     >>> utc_to_local('2000-03-12 07:00')
#     time.struct_time(tm_year=2000, tm_mon=3, tm_mday=11, tm_hour=23, tm_min=0, tm_sec=0, tm_wday=5, tm_yday=71, tm_isdst=0)
#     """

#     time_tuple = time.strptime(t, '%Y-%m-%d %I:%M')
#     secs = calendar.timegm(time_tuple)
#     return time.localtime(secs)
