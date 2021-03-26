import logging
import boto3
import os

def init_base():
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=os.environ['ENDPOINT_URL'])
    try:
        table = dynamodb.create_table(
            TableName=os.environ['CREATE_TABLE'],
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        logging.info('new database {} created'.format(os.environ['CREATE_TABLE']))
    except Exception as e:
        logging.info('load database {}'.format(os.environ['CREATE_TABLE']))
        table = dynamodb.Table(os.environ['CREATE_TABLE'])

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s:%(funcName)s:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    init_base()