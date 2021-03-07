# coding=utf-8
import time
import logging  
from concurrent import futures
import argparse

import grpc
from grpc_reflection.v1alpha import reflection

from configobj import ConfigObj
from prometheus_client import start_http_server, Summary, Counter
from py_grpc_prometheus.prometheus_server_interceptor import PromServerInterceptor

from processing_protos.processing_pb2 import Request, Response, DESCRIPTOR
from processing_protos.processing_pb2_grpc import (ProcessorServiceStub, 
    add_ProcessorServiceServicer_to_server, ProcessorServiceServicer)

from .processor import ModelProcessor

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
MAX_MSG_LENGTH = 100 * 1024 * 1024

model = None 
def init_prototype(config):
    global model
    model = ModelProcessor(config)

def run_prototype(text):
    return model(text)

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

FOUND = Counter('processor_count_found', 
                'Number of documents found')
CHECK = Counter('processor_count_check', 
                'Number of documents check')
ERROR = Counter('processor_count_error', 
                'Number of documents error')

class ProcessorService(ProcessorServiceServicer):
    @REQUEST_TIME.time()
    def ProcessData(self, request, context):
        FOUND.inc()
        text = request.Text
        logging.info('request data: size={}'.format(len(text)))
        
        start_time = time.time()
        try:
            result = run_prototype(text)

            logging.info('result: size={}'.format(len(result)))
         
            response = Response(Tokens=result)

            logging.info('response')
            CHECK.inc()
        except:
            ERROR.inc()
        return response


def serve(config):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)s: %(funcName)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('loading model')
    init_prototype(config)
    

    server = grpc.server(
        futures.ThreadPoolExecutor(
            max_workers=int(config['service']['max workers']),
        ),
        options=[('grpc.max_send_message_length', MAX_MSG_LENGTH),
                 ('grpc.max_message_length', MAX_MSG_LENGTH),
                 ('grpc.max_receive_message_length', MAX_MSG_LENGTH)],
        interceptors=(PromServerInterceptor(
        	enable_handling_time_histogram=True, legacy=True),) 
    )
    add_ProcessorServiceServicer_to_server(ProcessorService(), server)
    SERVICE_NAMES = (
        DESCRIPTOR.services_by_name['ProcessorService'].full_name,
        reflection.SERVICE_NAME,
    )

    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port(config['service']['port'])

    start_http_server(int(config['service']['prom port']))
    server.start()
    logging.info("Server running on port {}".format(config['service']['port']))

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to the config file')
    namespace = parser.parse_args()
    argv = vars(namespace)

    config = ConfigObj(infile=argv['config'], encoding='utf-8')

    serve(config)


if __name__ == '__main__':
    start()

