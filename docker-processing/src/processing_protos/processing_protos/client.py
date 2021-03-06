# coding=utf-8
import argparse

import time

import grpc

from .processing_pb2 import Request, Response
from .processing_pb2_grpc import ProcessorServiceStub

MAX_MSG_LENGTH = 30 * 1024 * 1024

class ProcessorClient(object):
    def __init__(self, address='localhost:9878'):
        self.address = address
        self.channel = grpc.insecure_channel(
            address, 
            options=[
            ('grpc.max_send_message_length', MAX_MSG_LENGTH),
            ('grpc.max_message_length', MAX_MSG_LENGTH),
            ('grpc.max_receive_message_length', MAX_MSG_LENGTH)
            ])
        self.stub = ProcessorServiceStub(self.channel)

    def process(self, text, timeout=None, address=None):
        request = Request(Text=text)

        response = self.stub.ProcessData.future(request).result(timeout)

        result = dict()
        result['tokens'] = list(response.Tokens)
        return result

def start():
    parser = argparse.ArgumentParser()
    parser.add_argument('text', help='text for processing')
    parser.add_argument('--server', default = 'localhost:9878', help='server host')
    namespace = parser.parse_args()
    argv = vars(namespace)
    
    client = ExampleClient(argv['server'])

    s = time.time()
    result = client.process(argv['text'])
    total_time = time.time() - s

    print('tokens: {}'.format(result['tokens']))
    print('time: {}'.format(total_time))

if __name__ == '__main__':
    start()