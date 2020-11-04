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
    * Should be formatted in RFC3339 format.
    * Should be converted from US/Pacific time to US/Eastern.
* `Address`
    * Should be passed through as is, except for Unicode validation.
* `ZIP`
    * Should be 5 digits.
    * Prepend with 0 if less than 5 digits.
* `FullName`
    * Should be converted to uppercase.
* `FooDuration` and `BarDuration`
    * Will be seconds, in floating point.
* `TotalDuration`
    * Sum of `FooDuration` and `BarDuration`.
* `Notes`
    * Should be passed through as is, except for Unicode validation.

## Working With Project

### Docker
This project is wired up to work with `Docker`. You aren't required to use it, but it can make
things easier.

The instructions in the next sections will include instructions for both `Docker` and a regular
python interpreter.

### Project Files
This section covers some of the high-level notes for some of the files included in this repo:

* `.coveragerc` - Contains settings for the test coverage plugin.
* `.dockerignore` - Contains patterns for files/directories to skip when copying files into the
        docker build context.
    * Note that this isn't used when mapping volumes into a container.
    * Note that the patterns in this file are mostly also covered in `.gitignore` so if you add
        patterns to this file, consider whether or not they should also go in the other one too.
* `.editorconfig` - Contains some settings for how files are treated to try to keep things
    consistent across people's different editor settings and IDEs.
* `.gitattributes` - Settings for how `git` should treat different files.
* `.gitignore` - Patterns for files/directories to avoid committing to the repository.
    * Note that the patterns in this file are mostly also covered in `.dockerignore` so if you add
        patterns to this file, consider whether or not they should also go in the other one too.
* `docker-compose.yaml` - Defines "services" to run our project, e.g. `app` to run local
    development and testing.
* `Dockerfile` - Defines the execution environment for our project, both locally and deployed.
* `Makefile` - Defines "targets" which are shortcuts of sorts, so instead of running something like:
        `docker-compose build --pull app` then `docker-compose up app`, you can just run
        `make build-local`
    * To see what shortcuts are available along with some help text, you can run `make help` on the
        command line.
    * Note that these are set up to work with Docker only.
* `pyproject.toml` - Defines settings for python tools, such as `black` and `pytest`.
* `requirements.txt` - Defines what packages and versions your project needs to run when deployed.
* `test_requirements.txt` - Defines packages and versions your project needs to run locally,
        meaning things like linting and testing packages.

### Local Setup
1. Docker:
    1. `make build-dev`
2. Python:
    1. `python3 -m venv venv`
    2. `. venv/bin/activate`
    3. `pip3 install -r test_requirements.txt`

### Normalize CSV File
1. Docker:
    1. `make normalize < my_csv.csv > output.csv`
1. Python:
    1. `PYTHONPATH=. python3 src/csv_normalizer.py < my_csv.csv > output.csv`

### Linting Code
This codebase is set up to lint the code using python [black](https://github.com/psf/black). To
lint do the following:

1. Docker:
    1. `make lint`
2. Python:
    1. `black .`
        1. If you want to see what it would change without actually changing the code, you can run
            it with the `--check` flag.

### Running tests
1. Docker:
    1. Run `make test`
        1. If you want to re-build the image (if you change `Dockerfile`), then you can run
            `make build-test`
        2. If you want to pass some options to `pytest`, you can run the command like this:
            `make test OPT="-s"`
2. Python:
    1. Run: `pytest`
        1. You can pass extra options to pytest like `pytest -s` to not run browser
            tests locally.

### Running code inside the container (Docker only)
If you want to be able to run things inside the container more than just running a single command,
    or to move around and see how things look, you can run this command:

1. `docker-compose run --rm app bash` or use the Makefile shortcut `make bash`
    1. `--rm` makes it so that the container gets deleted when you exit it. This can be useful to
        avoid cluttering up your host machine. If you care to keep the container, then take that
        part off.
    2. `app` is just the name of the service defined in `docker-compose.yaml`
    3. `bash` starts the command line session as a bash session.
