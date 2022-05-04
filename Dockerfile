FROM python:3.9-buster
ENV BOT_NAME=$BOT_NAME

WORKDIR /usr/src/

COPY requirements.txt /usr/src
RUN pip install -r /usr/src/requirements.txt
COPY . /usr
