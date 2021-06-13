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
FILE = None


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
    try:
        element = json.loads(body)

        if FILE is not None:
            FILE.writelines([json.dumps(element), '\n'])
        ch.basic_ack(delivery_tag=method.delivery_tag)

        logger.info(f' [✓] Received {body!r} on queue {QUEUE_NAME}')
    except json.decoder.JSONDecodeError:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        logger.info(f' [x] Rejected {body!r} on queue {QUEUE_NAME}')


def consume_queue():
    """Consumes from the queue using the callback."""
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

    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
    )

    logger.info(' [*] Waiting for messages on queue.')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception(e)
    finally:
        if channel.is_open:
            logger.debug('channel closed')
            channel.close()
        if connection.is_open:
            logger.debug('connection closed')
            connection.close()


if __name__ == '__main__':
    FILE = open(OUTPUT_FILE, 'a', buffering=1)
    consume_queue()
    if FILE is not None:
        FILE.close()
        logger.debug(f'{OUTPUT_FILE} closed')
