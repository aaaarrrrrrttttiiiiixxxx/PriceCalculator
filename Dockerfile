FROM python:3.11.1-slim

WORKDIR /

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src .

#RUN /bin/sh -c cd src
#RUN alembic upgrade head