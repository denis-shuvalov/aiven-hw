import asyncio
import random


async def test_is_alive(client):

    response = await client.get("/api/v1/system/is_alive")

    assert response.status == 200
    assert await response.json() == {"status": "ALIVE"}


async def test_data_exchange(client):

    response = await client.get("/api/v1/consumer/start")

    assert response.status == 200
    assert await response.json() == {"message": "Consumer started"}

    await asyncio.sleep(2)

    message = f"hello {random.randint(1,1000)}"
    response = await client.get(f"/api/v1/producer/send?message={message}")

    assert response.status == 200
    assert await response.json() == {"message": "Message has been sent"}

    await asyncio.sleep(2)

    response = await client.get("/api/v1/postgres/events?num_events=1")

    assert response.status == 200
    json_resp = await response.json()
    assert json_resp["events"][0] == message

