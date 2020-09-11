import json
import os
import requests

import boto3
from aws_lambda_powertools import Logger, Metrics, Tracer
from requests.structures import CaseInsensitiveDict

# https://awslabs.github.io/aws-lambda-powertools-python/#features
tracer = Tracer()
logger = Logger()
metrics = Metrics()

# Global variables are reused across execution contexts (if available)
session = boto3.Session()

@metrics.log_metrics(capture_cold_start_metric=True)
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event, context):
    get_page('https://app.plus500.com/')
    try:
        message = {"hello": "world"}
        return {
            "statusCode": 200,
            "body": json.dumps(message)
        }
    except Exception as e:
        logger.exception(e)
        raise

def get_page(url, fn=None, save=True):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    r = requests.get(url, headers=headers)
    print(r.text)