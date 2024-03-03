FROM alpine:latest

WORKDIR /app

RUN pip install -r requirements.txt
