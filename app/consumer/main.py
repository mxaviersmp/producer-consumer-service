import json
import pathlib

import pika

from app.utils.config import SETTINGS
from app.utils.logger import logger

USERNAME = SETTINGS.rabbitmq_default_user
PASSWORD = SETTINGS.rabbitmq_default_pass
HOST = SETTINGS.rabbitmq_host
RABBITMQ_CONNECTION_ATTEMPTS = SETTINGS.rabbitmq_connection_attempts
RABBITMQ_RETRY_DELAY = SETTINGS.rabbitmq_retry_delay
QUEUE_NAME = SETTINGS.rabbitmq_queue_name
OUTPUT_FILE = pathlib.Path().absolute() / 'output.txt'


def callback(
    ch: pika.adapters.blocking_connection.BlockingChannel,
    method: pika.spec.Basic.Deliver,
    properties: pika.spec.BasicProperties,
    body: bytes
):
    """
    Callback function to consume message from the queue.

    Collects message and saves to OUTPUT_FILE.
    """
    element = json.loads(body)

    file = open(OUTPUT_FILE, 'a')
    file.writelines([json.dumps(element), '\n'])
    file.close()

    logger.info(f' [x] Received {element} on queue {QUEUE_NAME}')


if __name__ == '__main__':
    credentials = pika.PlainCredentials(USERNAME, PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=HOST,
            credentials=credentials,
            connection_attempts=RABBITMQ_CONNECTION_ATTEMPTS,
            retry_delay=RABBITMQ_RETRY_DELAY,
        )
    )
    channel = connection.channel()
    logger.info(f'Connected pika consumer to {HOST}')

    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=True
    )

    logger.info(' [*] Waiting for messages on queue.')
    channel.start_consuming()
