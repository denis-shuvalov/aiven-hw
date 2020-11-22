from aiokafka import AIOKafkaProducer
import asyncio

loop = asyncio.get_event_loop()

async def send_one():
    producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers='broker:9092')
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait("in-topic", b"Super message")
        print("Sent")
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

if __name__ == "__main__":
    loop.run_until_complete(send_one())