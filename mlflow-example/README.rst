##############
MLflow Example
##############

Description
===========

Примеры использования библиотеки MLflow для построения отслеживаемых экспериментов по машинному обучению.

Запуск
===========

Сначала требуется выполнить некоторые экспорты (предполагается, что s3 сервер запущен, запущана база postgresql для MLflow, а также запущен mlflow server)

.. code-block:: bash

  export MLFLOW_TRACKING_URI=http://<ip mlflow server>:5000
  export AWS_ACCESS_KEY_ID=<access key to s3 where mlflow store artifacts>
  export AWS_SECRET_ACCESS_KEY=<secret access key to s3 where mlflow store artifacts>
  export AWS_DEFAULT_REGION=<s3 region>


Теперь можно запустить сам проект:

.. code-block:: bash

  mlflow run . --experiment-name <project name> -P C=0.5 -P penalty=l2
