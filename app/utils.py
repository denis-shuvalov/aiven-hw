import logging


async def consume_messages(consumer):
    async for msg in consumer:
        print("consumed: ", msg.topic, msg.partition, msg.offset,
              msg.key, msg.value, msg.timestamp)
