from aiohttp import web
from aiohttp.web import json_response


async def is_alive(request):
    return json_response(status=200, data={"status": "ALIVE"})