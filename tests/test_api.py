


async def test_status(client):

    response = await client.get("/api/v1/system/is_alive")

    assert response.status == 200
    assert await response.json() == {"status": "ALIVE"}

