FROM ubuntu:20.04

RUN apt update -yq && apt install -yq python3-pip nano git

COPY src/jupyter/requirements.txt /tmp/

RUN cat /tmp/requirements.txt | xargs --no-run-if-empty -n 1 python3 -m pip install \
    # clear pip cache
    && rm -rf /tmp/* /root/.cache/*

RUN mkdir /workspace
WORKDIR  /workspace
COPY ./config /config
COPY ./notebook /workspace/notebook


CMD ["python3" , "-m", "notebook", "--config", "/config/jupyter_notebook_config.py"]