# -*- coding: utf-8 -*-
"""
Tests for CSV Normalizer
"""
import csv
from io import StringIO

from _pytest.capture import CaptureFixture
from pytest_mock import MockFixture

from src.csv_normalizer import main


def test_outputs_normalized_csv(mocker: MockFixture, capsys: CaptureFixture[str]) -> None:
    with open("tests/sample.csv", encoding="utf-8", newline="") as csv_file:
        mocker.patch("sys.stdin", csv_file)

        main()

        captured = capsys.readouterr()

        assert len(captured.out) > 0
        assert len(captured.err) == 0

        written_csv = csv.reader(StringIO(captured.out))

        with open("tests/output-sample.csv", encoding="utf-8", newline="") as expected_csv_file:
            expected_csv = csv.reader(expected_csv_file)

            for written_line, expected_line in zip(written_csv, expected_csv):
                assert written_line == expected_line


def test_handles_error_properly(mocker: MockFixture, capsys: CaptureFixture[str]) -> None:
    with open("tests/sample-with-broken-fields.csv", encoding="utf-8", newline="") as csv_file:
        mocker.patch("sys.stdin", csv_file)

        main()

        captured = capsys.readouterr()

        assert len(captured.err) > 0

        expected_errors = [
            "Invalid timestamp: 4/1/11 11:00:00 �M",
            "invalid literal for int() with base 10: '9412�'",
            "Duration is in an invalid format: 123:32.123",
            "Duration has an invalid value: 1:a:32.123",
            "Duration is in an invalid format: 132:33.123",
            "Duration has an invalid value: 1:a:33.123",
        ]

        errors = captured.err.splitlines()

        assert len(errors) == len(expected_errors)

        for error, expected_error in zip(errors, expected_errors):
            assert error == expected_error

        assert len(captured.out) > 0

        written_csv = csv.reader(StringIO(captured.out))

        with open(
            "tests/output-sample-with-broken-fields.csv", encoding="utf-8", newline=""
        ) as expected_csv_file:
            expected_csv = csv.reader(expected_csv_file)

            for written_line, expected_line in zip(written_csv, expected_csv):
                assert written_line == expected_line
