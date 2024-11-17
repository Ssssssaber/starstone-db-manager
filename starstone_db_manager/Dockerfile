# Base
FROM python:3.11.5-alpine as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --update --virtual .build-deps \
build-base \
mysql-dev \
python3-dev 


RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Multistage
FROM python:3.11.5-alpine 
COPY --from=base /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/

RUN mkdir /logs
COPY . .