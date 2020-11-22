from aiokafka import AIOKafkaConsumer
import asyncio

loop = asyncio.get_event_loop()

async def consume():
    consumer = AIOKafkaConsumer(
        'in-topic',
        loop=loop, bootstrap_servers='broker:9092'
    )

    try:
        await consumer.start()
        # Consume messages
        print("consumer started")
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

if __name__ == "__main__":
    print("Start")
    loop.run_until_complete(consume())