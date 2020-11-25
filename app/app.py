import asyncio
import logging
from functools import partial
import signal
from aiohttp import web
import asyncpg
from aiokafka.helpers import create_ssl_context
from app import settings

from app.api.v1.system.view import is_alive
from app.api.v1.producer.view import send_to_kafka_topic
from app.api.v1.consumer.view import start_consumer, stop_consumer
from app.api.v1.postgres.view import get_events_from_pg

logging.basicConfig(level=logging.INFO)


def shutdown(app):

    if hasattr(app, "consumer"):
        app.consumer.stop()

    for task in asyncio.Task.all_tasks():
        task.cancel()


async def init_app(loop):

    app = web.Application(loop=loop)
    app.add_routes(
        [
            web.get('/api/v1/system/is_alive', is_alive),
            web.get('/api/v1/producer/send', send_to_kafka_topic),
            web.get('/api/v1/consumer/start', start_consumer),
            web.get('/api/v1/consumer/stop', stop_consumer),
            web.get('/api/v1/postgres/events', get_events_from_pg)
        ]
    )

    app.pool = await asyncpg.create_pool(
        dsn=settings.POSTGRES_URL,
        min_size=2,
        max_size=20,
        loop=loop
    )

    if settings.ENVIRONMENT == "aiven":
        app.ssl_context = create_ssl_context(
            cafile=settings.SSL_CAFILE_KAFKA,
            certfile=settings.SSL_CERTFILE_KAFKA,
            keyfile=settings.SSL_KEYFILE
        )
    else:
        app.ssl_context = None

    return app


def start():

    loop = asyncio.get_event_loop()

    app = loop.run_until_complete(init_app(loop))
    loop.add_signal_handler(signal.SIGHUP, partial(shutdown, app))
    loop.add_signal_handler(signal.SIGTERM, partial(shutdown, app))
    web.run_app(app, port=8080, host="0.0.0.0")


