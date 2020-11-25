import logging
import asyncpg

from app.settings import POSTGRES_URL, POSTGRES_TABLE


async def consume_messages(consumer):

    conn = await asyncpg.connect(POSTGRES_URL)
    async for msg in consumer:

        logging.info(msg=f"consumed:  {msg.value}")

        await conn.execute(
            f"""INSERT INTO {POSTGRES_TABLE} (topic, value)
                VALUES('{msg.topic}', '{msg.value.decode()}')
            """)

        logging.info(msg="Sent to postgres")


