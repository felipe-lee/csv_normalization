# -*- coding: utf-8 -*-
"""
Normalize CSV files
"""
import sys
from csv import DictWriter

from src.util import (
    convert_compact_duration_to_seconds,
    convert_datetime_to_timestamp,
    parse_timestamp,
    prepare_input_csv,
    process_zip_code,
    sum_durations,
)


def main() -> None:
    """
    Normalizes a csv input via stdin. Writes normalized csv to stdout. Writes any errors to stderr.
    """
    csv_reader = prepare_input_csv()

    csv_writer = DictWriter(f=sys.stdout, fieldnames=csv_reader.fieldnames)

    csv_writer.writeheader()

    for line in csv_reader:
        try:
            timestamp_dt = parse_timestamp(timestamp=line["Timestamp"])
        except ValueError as err:
            sys.stderr.write(f"{err}\n")

            continue

        try:
            zip_code = process_zip_code(input_zip=line["ZIP"])
        except ValueError as err:
            sys.stderr.write(f"{err}\n")

            continue

        try:
            foo_duration_seconds = convert_compact_duration_to_seconds(
                compact_duration=line["FooDuration"]
            )
        except ValueError as err:
            sys.stderr.write(f"{err}\n")

            continue

        try:
            bar_duration_seconds = convert_compact_duration_to_seconds(
                compact_duration=line["BarDuration"]
            )
        except ValueError as err:
            sys.stderr.write(f"{err}\n")

            continue

        csv_writer.writerow(
            {
                "Timestamp": convert_datetime_to_timestamp(input_datetime=timestamp_dt),
                "Address": line["Address"],
                "ZIP": zip_code,
                "FullName": line["FullName"].upper(),
                "FooDuration": foo_duration_seconds,
                "BarDuration": bar_duration_seconds,
                "TotalDuration": sum_durations(
                    duration_1=foo_duration_seconds, duration_2=bar_duration_seconds
                ),
                "Notes": line["Notes"],
            }
        )


if __name__ == "__main__":
    main()
