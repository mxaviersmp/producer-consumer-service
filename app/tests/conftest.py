import os

import pika
import pytest


@pytest.fixture(scope='session', autouse=True)
def tests_setup_and_teardown():
    """
    Fixture to be executed before and after tests.

    Connects to RabbitMQ server, then after test delete the queue.
    """
    queue_name = os.getenv('RABBITMQ_QUEUE_NAME')

    connection = pika.BlockingConnection()
    channel = connection.channel()

    yield

    channel.queue_delete(queue_name)
    channel.close()
    connection.close()
