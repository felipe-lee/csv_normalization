# -*- coding: utf-8 -*-
"""
Tests for util functions
"""
from datetime import datetime

import pytest
from pytest_mock import MockFixture

from src.csv_normalizer import prepare_input_csv
from src.util import (
    convert_compact_duration_to_seconds,
    convert_datetime_to_timestamp,
    parse_timestamp,
    process_zip_code,
    sum_durations,
)


class TestPrepareInputCSV:
    """
    Tests for prepare_input_csv
    """

    def test_returns_csv_from_stdin_as_dict_reader(self, mocker: MockFixture) -> None:
        with open("tests/sample.csv", newline="") as csv_file:
            mocker.patch("sys.stdin", csv_file)

            csv_reader = prepare_input_csv()

            item = next(csv_reader)

            assert item["Timestamp"] == "4/1/11 11:00:00 AM"
            assert item["Address"] == "123 4th St, Anywhere, AA"
            assert item["ZIP"] == "94121"
            assert item["FullName"] == "Monkey Alberto"
            assert item["FooDuration"] == "1:23:32.123"
            assert item["BarDuration"] == "1:32:33.123"
            assert item["TotalDuration"] == "zzsasdfa"
            assert item["Notes"] == "I am the very model of a modern major general"

    def test_replaces_invalid_character_with_unicode_replacement_character(
        self, mocker: MockFixture,
    ) -> None:
        # This file was saved in latin-1
        with open("tests/short-sample-broken-utf-8.csv", newline="") as csv_file:
            mocker.patch("sys.stdin", csv_file)

            csv_reader = prepare_input_csv()

            item = next(csv_reader)

            assert item["Notes"].endswith("�")


class TestParseTimestamp:
    """
    Tests for parse_timestamp
    """

    @pytest.mark.parametrize(
        "timestamp,datetime_object",
        (
            ("4/1/11 11:00:00 AM", datetime(2011, 4, 1, 11, 0, 0)),
            ("3/12/14 12:00:00 AM", datetime(2014, 3, 12, 0, 0, 0)),
            ("2/29/16 12:11:11 PM", datetime(2016, 2, 29, 12, 11, 11)),
            ("1/1/11 12:00:01 AM", datetime(2011, 1, 1, 0, 0, 1)),
            ("12/31/16 11:59:59 PM", datetime(2016, 12, 31, 23, 59, 59)),
            ("11/11/11 11:11:11 AM", datetime(2011, 11, 11, 11, 11, 11)),
            ("5/12/10 4:48:12 PM", datetime(2010, 5, 12, 16, 48, 12)),
            ("10/5/12 10:31:11 PM", datetime(2012, 10, 5, 22, 31, 11)),
            ("3/12/16 11:01:00 PM", datetime(2016, 3, 12, 23, 1, 0)),
        ),
    )
    def test_returns_expected_datetime_object(
        self, timestamp: str, datetime_object: datetime
    ) -> None:
        assert parse_timestamp(timestamp=timestamp) == datetime_object

    def test_raises_value_error_if_invalid_format(self) -> None:
        invalid_timestamp = "4/1/11 11:00:00 �"
        with pytest.raises(
            expected_exception=ValueError, match=rf"Invalid timestamp: {invalid_timestamp}"
        ):
            parse_timestamp(timestamp=invalid_timestamp)


class TestConvertDatetimeToTimestamp:
    """
    Tests for convert_datetime_to_timestamp
    """

    @pytest.mark.parametrize(
        "input_datetime,expected_timestamp",
        (
            (datetime(2011, 4, 1, 11, 0, 0), "2011-04-01T14:00:00-04:00"),
            (datetime(2014, 3, 12, 0, 0, 0), "2014-03-12T03:00:00-04:00"),
            (datetime(2016, 2, 29, 12, 11, 11), "2016-02-29T15:11:11-05:00"),
            (datetime(2011, 1, 1, 0, 0, 1), "2011-01-01T03:00:01-05:00"),
            (datetime(2016, 12, 31, 23, 59, 59), "2017-01-01T02:59:59-05:00"),
            (datetime(2011, 11, 11, 11, 11, 11), "2011-11-11T14:11:11-05:00"),
            (datetime(2010, 5, 12, 16, 48, 12), "2010-05-12T19:48:12-04:00"),
            (datetime(2012, 10, 5, 22, 31, 11), "2012-10-06T01:31:11-04:00"),
            (datetime(2016, 3, 12, 23, 1, 0), "2016-03-13T03:01:00-04:00"),
        ),
    )
    def test_converts_timestamp_to_rfc3339_and_eastern_time(
        self, input_datetime: datetime, expected_timestamp: str
    ) -> None:
        assert convert_datetime_to_timestamp(input_datetime=input_datetime) == expected_timestamp


class TestProcessZIPCode:
    """
    Tests for process_zip_code
    """

    @pytest.mark.parametrize(
        "input_zip,expected_zip", (("12345", "12345"), ("2345", "02345"), ("5", "00005"),)
    )
    def test_fills_zip_with_zeros_if_needed(self, input_zip: str, expected_zip: str) -> None:
        assert process_zip_code(input_zip=input_zip) == expected_zip

    def test_raises_value_error_for_invalid_zip(self) -> None:
        invalid_zip = "1234�"

        with pytest.raises(expected_exception=ValueError):
            process_zip_code(input_zip=invalid_zip)


class TestConvertCompactDurationToSeconds:
    """
    Tests for convert_compact_duration_to_seconds
    """

    @pytest.mark.parametrize(
        "compact_duration,expected_seconds",
        (
            ("1:23:32.123", 5012.123),
            ("1:32:33.123", 5553.123),
            ("111:23:32.123", 401012.123),
            ("31:23:32.123", 113012.123),
            ("0:00:00.000", 0.0),
        ),
    )
    def test_converts_compact_duration_to_seconds(
        self, compact_duration: str, expected_seconds: str
    ) -> None:
        assert (
            convert_compact_duration_to_seconds(compact_duration=compact_duration)
            == expected_seconds
        )

    @pytest.mark.parametrize(
        "duration,message",
        (
            ("1:2332.123", "Duration is in an invalid format: "),
            ("1:23�32.123", "Duration is in an invalid format: "),
            ("1:23:�2.123", "Duration has an invalid value: "),
        ),
    )
    def test_raises_value_error_if_invalid_format_or_value(
        self, duration: str, message: str
    ) -> None:
        with pytest.raises(expected_exception=ValueError, match=rf"{message}{duration}"):
            convert_compact_duration_to_seconds(duration)


class TestSumDurations:
    """
    Test for sum_durations
    """

    @pytest.mark.parametrize(
        "duration_1,duration_2,total_duration",
        (
            (5012.123, 5553.123, 10565.246),
            (401012.123, 5553.123, 406565.246),
            (113012.123, 5553.123, 118565.246),
            (5012.123, 0.0, 5012.123),
        ),
    )
    def test_calculates_expected_duration(
        self, duration_1: float, duration_2: float, total_duration: float
    ) -> None:
        assert sum_durations(duration_1=duration_1, duration_2=duration_2) == total_duration
