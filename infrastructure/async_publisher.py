import asyncio
import datetime
import json
from typing import List

import aiozmq
import zmq

from analytics.metric import MetricsRegistry
from infrastructure.boblogger import LogMessage


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

    async def publish_system_info(self):
        event = {
            "type": "export_system_info", }
        message = json.dumps(event)
        self.pub.write([message.encode()])
        print(f"Published event: {message}")


    async def flush_logs(self, logs: List[LogMessage]):

        data = [log.to_dict() for log in logs]
        event = {
            "type": "flush_logs",
            "data": data
        }
        message = json.dumps(event)

        self.pub.write([message.encode()])
        # print(f"Published event: {message}")

    async def flush_metrics(self, registry: MetricsRegistry):
        data = registry.get_metrics()
        event = {
            "type": "flush_metrics",
            "data": data
        }
        message = json.dumps(event)
        self.pub.write([message.encode()])
        print(f"Published event: {message}")

