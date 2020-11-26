from aiohttp.web import json_response, HTTPBadRequest
from app.api.v1.producer.model import send_to_kafka


async def send_to_kafka_topic(request):

    try:
        message = request.query["message"]
    except KeyError:
        return HTTPBadRequest()

    b_message = bytes(message, "utf-8")

    resp = await send_to_kafka(request, b_message)

    if resp == 0:
        return json_response(status=200, data={"message": "Message has been sent"})
    else:
        return json_response(status=500, data={"message": "Cannot connect to Kafka"})
