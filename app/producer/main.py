import json
from typing import Dict

from aio_pika import DeliveryMode, Message, connect_robust
from fastapi import FastAPI
from fastapi.responses import JSONResponse

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
    app.state.connection = await connect_robust(
        host=HOST,
        login=USERNAME,
        password=PASSWORD,
        connection_attempts=RABBITMQ_CONNECTION_ATTEMPTS,
        retry_delay=RABBITMQ_RETRY_DELAY,
    )
    app.state.channel = await app.state.connection.channel()
    logger.info(f'Connected pika producer to {HOST}')

    await app.state.channel.declare_queue(QUEUE_NAME, durable=True)


@app.on_event('shutdown')
async def shutdown():
    """
    Executes on application shutdown.

    Disconnects from RabbitMQ HOST.
    """
    app.state.connection.close()


@app.get('/')
async def root():
    """Root endpoint to check status."""
    return {'status': 'ok'}


@app.head('/')
def root_head():
    """Root endpoint HEAD."""
    return JSONResponse()


@app.post('/process')
async def process(valid_json: Dict):
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
    message = Message(
        json.dumps(valid_json, ensure_ascii=False).encode('utf-8'),
        delivery_mode=DeliveryMode.PERSISTENT
    )
    await app.state.channel.default_exchange.publish(
        message, routing_key=QUEUE_NAME
    )
    logger.info(f'Sent {valid_json} to queue {QUEUE_NAME}')
    return {'result': 'Success'}


@app.head('/process')
def process_head():
    """Process endpoint HEAD."""
    return JSONResponse()
