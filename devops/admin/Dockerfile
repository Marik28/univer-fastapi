FROM python:3.9-slim-buster

COPY requirements.txt requirements.txt

RUN pip3 install -U pip setuptools && \
    pip3 install -r requirements.txt && \
    rm requirements.txt

COPY src src
WORKDIR src