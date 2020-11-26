from aiohttp.web import json_response, HTTPBadRequest

from app.api.v1.postgres.model import get_last_events


async def get_events_from_pg(request):

    num_events = request.query.get("num_events")

    try:
        if int(num_events) < 0:
            return HTTPBadRequest()
    except ValueError:
        return HTTPBadRequest()

    async with request.app.pool.acquire() as conn:
        resp = await get_last_events(conn, num_events)

    return json_response(status=200, data={"events": resp})
