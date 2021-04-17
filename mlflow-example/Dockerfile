FROM ubuntu:20.04

RUN apt update -yq && apt install -yq python3-pip nano git

RUN python3 -m pip install -U numpy pandas scipy scikit-learn dvc mlflow boto3

RUN python3 -m pip install -U torch

RUN mkdir /app

WORKDIR /app