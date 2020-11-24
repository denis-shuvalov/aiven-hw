import logging
import asyncio
from aiohttp.web import json_response
from aiokafka import AIOKafkaConsumer
from kafka.errors import KafkaConnectionError
from app import settings

from app.utils import consume_messages


async def start_consumer(request):

    if hasattr(request.app, "cons_task"):
        await request.app.consumer.stop()
        request.app.cons_task.cancel()

    loop = asyncio.get_event_loop()

    request.app.consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        loop=loop,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER
    )

    try:
        await request.app.consumer.start()
        request.app.cons_task = loop.create_task(consume_messages(request.app.consumer))
        logging.info(msg="Consumer started")
        return json_response(status=200, data={"message": "Consumer started"})

    except KafkaConnectionError:
        logging.warning(msg="Consumer can not connect to kafka")
        await request.app.consumer.stop()

        return json_response(status=500, data={"message": "Consumer can not connect to Kafka"})


async def stop_consumer(request):

    await request.app.consumer.stop()
    request.app.cons_task.cancel()

    logging.info(msg="Consumer stopped.")
    return json_response(status=200, data={"message": "Consumer stopped"})