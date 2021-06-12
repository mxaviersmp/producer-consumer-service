import json
from typing import Dict

import pika
from fastapi import FastAPI

from app.utils.config import SETTINGS
from app.utils.logger import logger

USERNAME = SETTINGS.rabbitmq_default_user
PASSWORD = SETTINGS.rabbitmq_default_pass
HOST = SETTINGS.rabbitmq_host
RABBITMQ_CONNECTION_ATTEMPTS = SETTINGS.rabbitmq_connection_attempts
RABBITMQ_RETRY_DELAY = SETTINGS.rabbitmq_retry_delay
QUEUE_NAME = SETTINGS.rabbitmq_queue_name

app = FastAPI()


@app.on_event('startup')
async def startup():
    """
    Executes on application startup.

    Connects to RabbitMQ HOST and to the channel QUEUE_NAME.
    """
    credentials = pika.PlainCredentials(USERNAME, PASSWORD)
    app.state.connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=HOST,
            credentials=credentials,
            connection_attempts=RABBITMQ_CONNECTION_ATTEMPTS,
            retry_delay=RABBITMQ_RETRY_DELAY,
        )
    )
    app.state.channel = app.state.connection.channel()
    logger.info(f'Connected pika producer to {HOST}')

    app.state.channel.queue_declare(queue=QUEUE_NAME)


@app.on_event('shutdown')
async def shutdown():
    """
    Executes on application shutdown.

    Disconnects from RabbitMQ HOST.
    """
    app.state.connection.close()


@app.get('/')
def read_root():
    """Root endpoint to check status."""
    return {'status': 'ok'}


@app.post('/process')
def process(valid_json: Dict):
    """
    Published a json message to the queue.

    Parameters
    ----------
    valid_json : json
        valid json entry

    Returns
    -------
    json
        Success result if added to queue successfull
    """
    app.state.channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(valid_json)
    )
    logger.info(f'Sent {valid_json} to queue {QUEUE_NAME}')
    return {'result': 'Success'}
