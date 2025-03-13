FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN apk add --no-cache bash
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc python3-dev libc-dev linux-headers postgresql-dev musl-dev \
        libjpeg-turbo-dev zlib zlib-dev

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps


RUN mkdir /app
WORKDIR /app

COPY wait-for-it.sh /app/
RUN chmod +x /app/wait-for-it.sh
COPY . .

RUN adduser -D user
USER user
