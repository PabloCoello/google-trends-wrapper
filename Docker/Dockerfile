FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    python3.8 \
    python3-pip \
    libpq-dev 

RUN python3 -m pip install pytrends \
    pandas \
    operator

RUN mkdir -p /local/lib/python3.8/dist-packages/

ENV PYTHONPATH=/local/lib/python3.8/dist-packages/

WORKDIR /opt/google-trends-wrapper/