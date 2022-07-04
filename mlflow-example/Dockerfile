FROM ubuntu:20.04

RUN apt update -yq && apt install -yq python3-pip nano git

RUN python3 -m pip install -U numpy==1.21.2 pandas==1.3.2 scipy==1.7.1 scikit-learn==0.24.2 mlflow==1.20.1 boto3 dvc[s3]==2.6.4 protobuf==3.20.1

RUN python3 -m pip install -U torch==1.9.0

RUN mkdir /app

WORKDIR /app