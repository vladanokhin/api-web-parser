FROM python:3.8.10-slim

WORKDIR /var/www/html/

COPY requirements.txt .

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y update && apt-get install -y --no-install-recommends \
    python3-pip python3-dev firefox-esr/oldstable


RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt

ENTRYPOINT gunicorn -w 4 --reload --timeout ${WORKER_TIMEOUT} --bind ${FLASK_HOST}:${FLASK_PORT} main:app
