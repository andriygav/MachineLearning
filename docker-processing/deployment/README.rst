Instalation
===========

Деплоя сервиса в k8s выполняется при помощи репозитория сервисов *helm*

.. code-block:: bash

    helm repo add tokenizer helm repo add tokenizer git+https://github.com/andriygav/MachineLearning@docker-processing/deployment
    helm repo update
    helm search repo tokenizer
    helm install tokenizer tokenizer/tokenizer -n namespace

Где *namespace* уже сущестувующее пространство на кластере, где будет размещен сервис.
