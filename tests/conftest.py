import pytest
from aiohttp import web
from app.api.v1.system.view import is_alive
from app.api.v1.producer.view import send_to_kafka_topic
from app import settings


@pytest.fixture
def client(loop, aiohttp_client):
    app = web.Application()
    app.router.add_get('/api/v1/system/is_alive', is_alive)
    app.router.add_view('/api/v1/producer/send', send_to_kafka_topic)
