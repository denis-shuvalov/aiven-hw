import asyncio
import logging
from aiohttp import web

from app import settings
from aiokafka import AIOKafkaConsumer

from app.api.v1.system.view import is_alive
from app.api.v1.producer.view import send_to_kafka_topic
from app.api.v1.consumer.view import start_consumer, stop_consumer


async def stop_connection(app):

    app.consumer.stop()


async def init_app(loop):

    app = web.Application(loop=loop)

    app.consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        loop=loop,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER
    )
    await app.consumer.start()
    logging.info(msg="Consumer started")
    app.add_routes(
        [
            web.get('/api/v1/system/is_alive', is_alive),
            web.get('/api/v1/producer/send', send_to_kafka_topic),
            web.get('/api/v1/consumer/start', start_consumer),
            web.get('/api/v1/consumer/stop', stop_consumer)
        ]
    )

    app.on_shutdown.append(stop_connection(app))


    return app


def start():

    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app(loop))
    web.run_app(app, port=8080, host="0.0.0.0")
