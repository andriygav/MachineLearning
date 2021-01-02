FROM ubuntu:20.04

RUN apt update -yq && apt install -yq python3-pip nano

RUN python3 -m pip install -U numpy scipy scikit-learn mlflow boto3

RUN mkdir /app

WORKDIR /app