#FROM ubuntu:latest
#LABEL authors="Aleksej"

#ENTRYPOINT ["top", "-b"]

FROM python:3.11
WORKDIR /api

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt