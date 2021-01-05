##############
MLflow Example
##############

Description
===========

Примеры использования библиотеки MLflow для построения отслеживаемых экспериментов по машинному обучению.

Запуск
===========
Перед работой требуется настройка mlflow сервера для дальнейшей работы:

- Выделить s3 storage для хранения версионированых моделей (убедится что хранилище доступно, добавить параметры окружения, чтобы работало через ``boto3``).
- Создать postgresql сервер для хранения всей метаинформации о экспериментах. Внутри сервера создать базу данных ``mlflow``
- Запустить mlflow server

.. code-block:: bash

  nohup mlflow server --host 0.0.0.0 --default-artifact-root s3://<your bucket name> --backend-store-uri postgresql://<user>:<password>@<url>:5432/mlflow &>out&

Вычислитель на локальном компютере
----------------------------------

Сначала требуется выполнить некоторые экспорты:

.. code-block:: bash

  export MLFLOW_TRACKING_URI=http://<ip mlflow server>:5000
  export AWS_ACCESS_KEY_ID=<access key to s3 where mlflow store artifacts>
  export AWS_SECRET_ACCESS_KEY=<secret access key to s3 where mlflow store artifacts>
  export AWS_DEFAULT_REGION=<s3 region>

Теперь можно запустить сам проект:

.. code-block:: bash

  mlflow run . --experiment-name <project name> -P C=0.5 -P penalty=l2

Вычислитель на k8s
------------------
В данном пункте будет предложена инструкция как выполнять mlflow project на удаленном k8s сервере. Данная инструкция является расширеной версией документации. 

Настройка k8s
*************
Если k8s сервер уже настроен, то данный пункт может быть пропущен.

В данном примере в качестве простого k8s класстера использовался ``microk8s``.
Для установки и настроек требуется выполнить следующие комманды (подробнее на `сайте <https://logz.io/blog/getting-started-with-kubernetes-using-microk8s/>`_.):

- Комманда для установки ``microk8s`` через ``snap``:

.. code-block:: bash

  sudo snap install microk8s --classic --channel=1.16/stable
  
- Проверить, что ``microk8s`` запущен можно следующим образом:

.. code-block:: bash

  sudo microk8s.status
  
- Для удобного отслеживания можно включить специальный ``dashboard``:

.. code-block:: bash

  sudo microk8s.enable dns dashboard ingress 
  
- Также выполним дополнительную настройку, чтобы заходить для отслеживания можно было без токена:

.. code-block:: bash

  sudo microk8s.kubectl -n kube-system edit deploy kubernetes-dashboard -o yaml 
  # в появившемся файле добавить строчку --enable-skip-login как показано ниже
  #...
  spec:
      containers:
      - args:
        - --auto-generate-certificates
        - --namespace=kube-system
        - --enable-skip-login
  #...
  
- По дефолту ``dashboard`` доступен только из локального компютера. Разрешим доступ из вне:

.. code-block:: bash

  sudo microk8s.kubectl proxy --accept-hosts=.* --address=0.0.0.0 &

  
- Удобный ``dashboard`` доступный по ссылке:

.. code-block:: bash

   http://<kubernetes ip>:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/
   
Сервис ``k8s`` запущен и с ним можно работать. Теперь требуется выполнить настройку ``k8s`` под mlflow:

- Добавить специальный ``namespace`` mlflow в котором и будет выполняться работа

.. code-block:: bash

  sudo microk8s.kubectl create namespace mlflow
  
- Для доступа к s3 требуются ``credentionals`` их обычно хранят в cluster config map (если проверить kubernetes_job_template.yaml, то там параметр окружения задается из configMap на кластере). Создадим нужный нам configmap ``credentionals``

.. code-block:: bash

  # создать файл
  touch credentials.yaml
  # в него записать все нужные параметры
  # должен выглядеть как-то так
  cat credentials.yaml
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: credentials
    namespace: grabovoy
  data:
    AWS_ACCESS_KEY_ID: "<access key to s3 where mlflow store artifacts>"
    AWS_DEFAULT_REGION: "<s3 region>"
    AWS_SECRET_ACCESS_KEY: "<secret access key to s3 where mlflow store artifacts>"
  
  sudo microk8s.kubectl apply -f credentials.yaml 

Теперь кластер ``microk8s`` полностью готов к работе.

Запуск проекта на удаленном k8s сервере
***************************************
Сначала требуется получить доступ к удаленному кластеру. В случае если есть доступ к кластеру, который запущен через ``microk8s``, то конфиг можно получить командой 

.. code-block:: bash

  sudo microk8s.config
  
Все содержимое файла требуется сохранить в файл ``~/.kube/config``. ВАЖНО! Текущая версия kubernetes-client для python не поддерживает передачи пути к конфигурационному файлу через параметр окружения ``KUBECONFIG``.

Теперь к удаленному кластеру есть доступ через python, а следовательно mlflow также может выполнить удаленную задачу на кластере.

Теперь требуется получить доступ к docker hub. Хранилище докер контейнеров нужно для передачи докер контейнера с локального компютера на кластер. MLflow собирает докер со всеми файлами локально на компютере, после чего помещает его в docker hub и дает запрос на k8s кластер, который создает Job с указаным контейнером, предварительно скачивая его из docker hub.

Для получения доступа, требуется просто выполнить комманду:

.. code-block:: bash

  sudo docker login
  
Все настройки компютера завершены, теперь можно создавать задачи, которые будут выполняться на удаленном кластере (возможно понадобиться sudo для соборки докера, либо выдать доступ к докеру текущему пользователю):

.. code-block:: bash

  export MLFLOW_TRACKING_URI=http://<ip mlflow server>:5000
  mlflow run . --experiment-name <project name> -P C=0.5 -P penalty=l2 --backend kubernetes --backend-config kubernetes_config.json
  
  
После запуск начнеться сборка докера и поставка его в docker hub, после чего будет дан запрос на cluster. ВАЖНО! Операция является блокирующей (ждет пока на кластере завершиться запрошенная задача), поэтому рекомендуется использовать nohup.
