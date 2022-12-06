FROM python:3.8.10

ENV PYTHONBUFFERED 1

RUN mkdir /convo-web

WORKDIR /convo-web

COPY . .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2-binary \
    && pip install pillow

RUN pip install -r req.txt

EXPOSE 8000