# CSV Normalization

## Introduction

Python code to normalize a CSV file.

## Background
This is a tool that reads a CSV formatted file on `stdin` and emits a normalized CSV formatted file
on `stdout`.

### Input
* Input file should be in UTF-8
* Times are in US/Pacific.
* The [sample data](tests/sample.csv) contains all date and time format variants possible.

### Output
Output file should be a CSV file that has been normalized.

Normalized, in this case, means:

* The entire CSV is in the UTF-8 character set.
    * If a character is invalid, it will be replaced with the Unicode Replacement Character.
        * If that replacement makes data invalid (for example, because it turns a date field into
            something unparseable), a warning will be printed to `stderr` and the row will be
            absent from the output.
* `Timestamp`
    * Output column should be formatted in RFC3339 format.
    * Should be converted from US/Pacific time to US/Eastern.
* `Address`
    * Should be passed through as is, except for Unicode validation.
* `ZIP`
    * Should be 5 digits.
    * Prepend with 0 if less than 5 digits.
* `FullName`
    * Will be full uppercase.
* `FooDuration` and `BarDuration`
    * Durations will be seconds, in floating point.
* `TotalDuration`
    * Sum of `FooDuration` and `BarDuration`.
* `Notes`
    * Invalid UTF-8 characters, will be replaced with the Unicode Replacement Character.
