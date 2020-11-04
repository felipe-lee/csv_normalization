# -*- coding: utf-8 -*-
"""
Utility helper functions
"""
import sys
from csv import DictReader
from datetime import datetime
from io import TextIOWrapper

from dateutil.parser import ParserError, parse
from dateutil.tz import gettz


def prepare_input_csv() -> DictReader:
    """
    Reads csv file from stdin with utf-8 encoding escaping errors with the Unicode Replacement
    Character: �

    Returns:
        CSV DictReader instance with stdin contents
    """
    fixed_input = TextIOWrapper(buffer=sys.stdin.buffer, encoding="utf-8", errors="replace")

    return DictReader(fixed_input)


def parse_timestamp(timestamp: str) -> datetime:
    """
    Parses input timestamp string into a native datetime object.

    Args:
        timestamp: Timestamp string. Format can vary. Ex: "4/1/11 11:00:00 AM"

    Returns:
        datetime representation of input timestamp

    Raises:
        ValueError: If timestamp is in a format that can't be parsed by dateutil.parser.parse
    """
    try:
        return parse(timestr=timestamp)
    except ParserError:
        raise ValueError(f"Invalid timestamp: {timestamp}")


def convert_datetime_to_timestamp(input_datetime: datetime) -> str:
    """
    Converts a datetime object (US/Pacific) to an RFC3339 formatted timestamp in US/Eastern time.

    Args:
        input_datetime: datetime object. Should be in US/Pacific (whether it's aware or not)

    Returns:
        RFC3339 formatted timestamp in US/Eastern time.
    """
    us_pacific_tz = gettz("US/Pacific")
    us_eastern_tz = gettz("US/Eastern")

    pacific_dt = input_datetime.replace(tzinfo=us_pacific_tz)

    eastern_dt = pacific_dt.astimezone(tz=us_eastern_tz)

    return eastern_dt.isoformat()


def process_zip_code(input_zip: str) -> str:
    """
    Audits ZIP code and zero-fills (as prefix) if necessary

    Args:
        input_zip: zip to audit and z-fill

    Returns:
        ZIP code of 5 digits, with leading zeros if needed.

    Raises:
        ValueError: If input_zip isn't numeric
    """
    int(input_zip)

    return input_zip.zfill(5)


def convert_compact_duration_to_seconds(compact_duration: str) -> float:
    """
    Converts a duration in hours, min, sec, and ms to seconds.

    Args:
        compact_duration: duration in hours, minutes, seconds, and milliseconds. Hrs, min, and sec
            separated by ":", while sec and ms are separated by "."
            E.g. "1:23:32.123"

    Returns:
        duration in milliseconds

    Raises:
        ValueError: If any part of the duration doesn't match expected format or has an invalid
            value.
    """
    try:
        hours, minutes, seconds = compact_duration.split(":")
    except ValueError:
        raise ValueError(f"Duration is in an invalid format: {compact_duration}")

    try:
        hours, minutes, seconds = map(float, [hours, minutes, seconds])
    except ValueError:
        raise ValueError(f"Duration has an invalid value: {compact_duration}")

    return (hours * 3600) + (minutes * 60) + seconds


def sum_durations(duration_1: float, duration_2: float) -> float:
    """
    Sums two float durations and handles cutting off imprecise bits.

    Args:
        duration_1: first duration in seconds
        duration_2: second duration in seconds

    Returns:
        total duration in seconds
    """
    total_duration = duration_1 + duration_2

    total_duration_fixed = format(total_duration, ".3f")

    return float(total_duration_fixed)
