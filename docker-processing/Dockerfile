FROM ubuntu:20.04

RUN apt update -yq && apt install -yq python3-pip nano git

COPY src/processing_protos/requirements.txt /tmp/

RUN cat /tmp/requirements.txt | xargs --no-run-if-empty -n 1 python3 -m pip install \
    # clear pip cache
    && rm -rf /tmp/* /root/.cache/*

COPY src/processing/requirements.txt /tmp/

RUN cat /tmp/requirements.txt | xargs --no-run-if-empty -n 1 python3 -m pip install \
    # clear pip cache
    && rm -rf /tmp/* /root/.cache/*

RUN mkdir /app
COPY ./src /app/src
COPY ./config /config

RUN python3 -m pip install /app/src/processing_protos
RUN python3 -m pip install /app/src/processing

WORKDIR  /app


CMD ["python3" , "-m", "processing.service", "/config/config.cfg"]