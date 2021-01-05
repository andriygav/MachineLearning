import pickle
import argparse

import dvc.api
import mlflow
from mlflow import log_metric, log_param, log_artifacts

import pandas
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--C', type=float, default = 1.0, help='inverse of regularization strength')
    parser.add_argument('--penalty', default = 'l2', choices=['l1','l2'], help='the norm used in the penalization')
    namespace = parser.parse_args()
    argv = vars(namespace)

    with dvc.api.open(
        'mlflow-example/data/dataset.csv',
        repo='https://github.com/andriygav/MachineLearning'
        ) as f:
        dataset = pd.read_csv(f)

    with mlflow.start_run():

        X, Y = dataset.values[:,:2], dataset.values[:,2]
        X_train, X_test, Y_train, Y_test = train_test_split(
            X, Y, test_size=100, random_state=0)

        log_param("C", argv['C'])
        log_param("penalty", argv['penalty'])

        model = LogisticRegression(C=argv['C'], penalty=argv['penalty'], solver='saga')

        model.fit(X_train, Y_train)

        with open('./model.pkl', 'wb') as f:
            pickle.dump(model, f)

        log_metric("train acc", model.score(X_train, Y_train))
        log_metric("test acc", model.score(X_test, Y_test))

        mlflow.log_artifact(local_path = './model.pkl', artifact_path='model')

        mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                registered_model_name="test_model", await_registration_for=0
            )
