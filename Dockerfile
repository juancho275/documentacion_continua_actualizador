# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

RUN apt-get update -y && apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /requirements.txt
WORKDIR /
RUN pip3 install -r requirements.txt
COPY . /
EXPOSE 8000
RUN  apt install -y curl 
CMD [ "python3", "ActualizadorAzureDevops.py"]

