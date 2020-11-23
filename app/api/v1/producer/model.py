import logging

from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaConnectionError

from app import settings


async def send_to_kafka(request, message):

    producer = AIOKafkaProducer(
        loop=request.app.loop,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER
    )

    try:
        await producer.start()
        await producer.send_and_wait(settings.KAFKA_TOPIC, message)
        logging.info(f"Message '{message}' is sent")
        return 0
    except KafkaConnectionError:
        logging.warning(msg="Can not connect to kafka")
        return -1
    finally:
        await producer.stop()
