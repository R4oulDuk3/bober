import asyncio
import datetime
import json


import aiozmq
import zmq


class AsyncPublisher:
    def __init__(self, publish_address: str):
        self.publish_address = publish_address
        self.pub = None

    async def connect(self):
        self.pub = await aiozmq.create_zmq_stream(
            zmq.PUB,
            bind=self.publish_address,
            loop=asyncio.get_event_loop()
        )
        print("Publisher connected and ready")

    async def publish_telemetry(self, data: dict):
        event = {
            "type": "export_telemetry",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "data": data
        }
        message = json.dumps(event)
        self.pub.write([message.encode()])
        print(f"Published telemetry: {message}")

    async def publish_event(self, event_name: str, data: dict):
        event = {
            "type": "export_event",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "event": event_name,
            "data": data
        }
        message = json.dumps(event)
        self.pub.write([message.encode()])
        print(f"Published event: {message}")