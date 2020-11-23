import logging
import asyncio
from aiohttp.web import json_response
from kafka.errors import KafkaConnectionError

from app.utils import consume_messages


async def start_consumer(request):

    consumer = request.app.consumer
    loop = asyncio.get_event_loop()

    try:
        loop.create_future(consume_messages(consumer))
        return json_response(status=200, data={"message": "Consumer started"})

    except KafkaConnectionError:
        logging.warning(msg="Consumer can not connect to kafka")
        return json_response(status=500, data={"message": "Consumer can not connect to Kafka"})

    finally:
        await consumer.stop()


async def stop_consumer(request):

    await request.app.consumer.stop()

    return json_response(status=200, data={"message": "Consumer stopped"})