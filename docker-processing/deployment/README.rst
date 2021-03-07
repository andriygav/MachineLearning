Instalation
===========

Деплоя сервиса в k8s выполняется при помощи репозитория сервисов *helm*

.. code-block:: bash

    helm repo add tokenizer https://raw.githubusercontent.com/andriygav/MachineLearning/master/docker-processing/deployment/
    helm repo update
    helm install tokenizer tokenizer/tokenizer -n namespace

Где *namespace* уже сущестувющее пространство на кластере, где будет размещен сервис.