# This is only meant to be used for local development and testing.
FROM python:3.8

ENV PROJECT_PATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

ENV PYTHONPATH=${PROJECT_PATH}:${PYTHONPATH}

WORKDIR ${PROJECT_PATH}

COPY *requirements.txt ./

RUN pip install -r test_requirements.txt
