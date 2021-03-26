FROM ubuntu:20.04

RUN apt update -yq && apt install -yq python3-pip nano git

COPY src/dynamodb/requirements.txt /tmp/

RUN cat /tmp/requirements.txt | xargs --no-run-if-empty -n 1 python3 -m pip install \
    # clear pip cache
    && rm -rf /tmp/* /root/.cache/*

RUN mkdir /app
WORKDIR  /app

COPY data/init.py /app/init.py

CMD ["python3",  "init.py"]