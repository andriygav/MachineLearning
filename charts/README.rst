Instalation
===========

Деплоя сервиса в k8s выполняется при помощи репозитория сервисов *helm*

.. code-block:: bash

    helm repo add <my repo name> git+https://github.com/andriygav/MachineLearning@/charts
    helm repo update
    helm search repo <my repo name>
    helm install tokenizer <my repo name>/tokenizer -n namespace

Где *namespace* уже сущестувующее пространство на кластере, где будет размещен сервис.
