import json
from datetime import datetime
import zmq


class SyncPublisher:
    def __init__(self, publish_address: str):
        self.publish_address = publish_address
        self.context = zmq.Context()
        self.pub = self.context.socket(zmq.PUB)

    def connect(self):
        self.pub.bind(self.publish_address)
        print("Publisher connected and ready")

    def publish_telemetry(self, data: dict):
        event = {
            "type": "export_telemetry",
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        message = json.dumps(event)
        self.pub.send_string(message)
        print(f"Published telemetry: {message}")

    def publish_event(self, event_name: str, data: dict):
        event = {
            "type": "export_event",
            "timestamp": datetime.now().isoformat(),
            "event": event_name,
            "data": data
        }
        message = json.dumps(event)
        self.pub.send_string(message)
        print(f"Published event: {message}")

    def close(self):
        if self.pub:
            self.pub.close()
        if self.context:
            self.context.term()