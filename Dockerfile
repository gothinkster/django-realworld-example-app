FROM python:3.5-slim-stretch

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
