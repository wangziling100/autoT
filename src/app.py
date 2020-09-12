import json
import os
import requests
import random

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
    headers = get_headers()
    r = requests.get(url, headers=headers)
    print(r.text)

def get_headers():
    headers = CaseInsensitiveDict()
    browser_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .\
            NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)', ]
    headers['User-Agent'] = random.choice(browser_list)
    headers["Accept"] = "application/json"
    return headers 