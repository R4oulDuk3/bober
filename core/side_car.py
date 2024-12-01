import asyncio
import json
import aiozmq
import zmq


class SideCarExporter:
    def __init__(self):
        self.metrics = {}

    async def process_metric(self, event):
        event_type = event['type']

        if event_type == 'export_telemetry':
            print(f"TELEMETRY: timestamp={event['timestamp']}")
            print(f"DATA: {json.dumps(event['data'], indent=2)}")
            print("-" * 50)

        elif event_type == 'export_event':
            print(f"EVENT: {event['event']}")
            print(f"TIMESTAMP: {event['timestamp']}")
            print(f"DATA: {json.dumps(event['data'], indent=2)}")
            print("-" * 50)


class AsyncSubscriber:
    def __init__(self, exporter: SideCarExporter, listen_address: str):
        self.exporter = exporter
        self.tasks = set()
        self.listen_address = listen_address
        self.sub = None

    async def connect(self):
        self.sub = await aiozmq.create_zmq_stream(
            zmq.SUB,
            connect=self.listen_address,
            loop=asyncio.get_event_loop()
        )
        self.sub.transport.subscribe(b'')
        print("Subscriber connected and ready")

    async def process_message(self, message):
        try:
            event = json.loads(message.decode())
            await self.exporter.process_metric(event)
        except Exception as e:
            print(f"Error processing message: {e}")

    def create_task(self, message):
        task = asyncio.create_task(self.process_message(message))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

    async def run(self):
        await self.connect()
        try:
            while True:
                message = await self.sub.read()
                if message:
                    self.create_task(message[0])
        except asyncio.CancelledError:
            print("Subscriber shutdown initiated")
        finally:
            self.sub.close()
            if self.tasks:
                await asyncio.gather(*self.tasks, return_exceptions=True)


async def main():
    metrics_collector = SideCarExporter()
    subscriber = AsyncSubscriber(metrics_collector, listen_address="tcp://127.0.0.1:5555")
    try:
        await subscriber.run()
    except KeyboardInterrupt:
        print("Shutting down...")


if __name__ == "__main__":
    asyncio.run(main())