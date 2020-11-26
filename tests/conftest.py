import asyncpg
import pytest
from aiohttp import web
from aiokafka.helpers import create_ssl_context

from app.api.v1.system.view import is_alive
from app.api.v1.producer.view import send_to_kafka_topic
from app.api.v1.consumer.view import start_consumer, stop_consumer
from app.api.v1.postgres.view import get_events_from_pg
from app import settings


@pytest.fixture
def client(loop, aiohttp_client):
    app = web.Application()
    app.add_routes(
        [
            web.get('/api/v1/system/is_alive', is_alive),
            web.get('/api/v1/producer/send', send_to_kafka_topic),
            web.get('/api/v1/consumer/start', start_consumer),
            web.get('/api/v1/consumer/stop', stop_consumer),
            web.get('/api/v1/postgres/events', get_events_from_pg)
        ]
    )

    app.pool = loop.run_until_complete(
        asyncpg.create_pool(
            dsn=settings.POSTGRES_URL,
            min_size=2,
            max_size=20,
            loop=loop
        )
    )

    if settings.ENVIRONMENT == "aiven":
        app.ssl_context = create_ssl_context(
            cafile=settings.SSL_CAFILE_KAFKA,
            certfile=settings.SSL_CERTFILE_KAFKA,
            keyfile=settings.SSL_KEYFILE
        )
    else:
        app.ssl_context = None

    yield loop.run_until_complete(aiohttp_client(app))

    if hasattr(app, "consumer"):
        loop.run_until_complete(app.consumer.stop())

    loop.run_until_complete(app.pool.close())
