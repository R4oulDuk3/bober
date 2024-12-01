import asyncio
import json

import aiohttp
import aiozmq
import zmq

from analytics.analytics_client import MachineIoTClient
from core.system_info import get_system_info_string, get_system_info


class SideCarExporter:
    def __init__(self, analytics_client: MachineIoTClient = MachineIoTClient.produce(), backend_host = "http://10.0.4.62:80"):
        self.analytics_client = analytics_client
        self.backend_host = backend_host

    async def process_metric(self, event):
        event_type = event['type']

        if event_type == 'export_telemetry':
            data = event['data']

            print(f"TELEMETRY: timestamp={event['timestamp']}")
            print(f"DATA: {json.dumps(data, indent=2)}")
            print("-" * 50)
            total_output_unit_count=  data["totaloutputunitcount"]
            machine_speed= data["machinespeed"]
            timestamp = event['timestamp']
            await self.analytics_client.send_telemetry(
                timestamp=timestamp,
                machine_speed=machine_speed,
                total_output_unit_count=total_output_unit_count,
            )


        elif event_type == 'export_event':
            print(f"EVENT: {event['event']}")
            data = event['data']

            print(f"TIMESTAMP: {event['timestamp']}")
            print(f"DATA: {json.dumps(event['data'], indent=2)}")
            print("-" * 50)
            total_output_unit_count = data["totaloutputunitcount"]
            machine_speed = data["machinespeed"]
            timestamp = event['timestamp']
            event = event['event']
            await self.analytics_client.send_machine_event(
                timestamp=timestamp,
                machine_speed=machine_speed,
                total_output_unit_count=total_output_unit_count,
                event_type=event,
                job_id="job_id"
            )
        elif event_type == "export_system_info":
            print("Received export_system_info event")
            try:
                info = get_system_info()
                async with aiohttp.ClientSession() as session:
                    await session.post(
                        url=f"{self.backend_host}/api/v1/system/info",
                        json=info
                    )
                    print(f"Sent system info to backend {info}" )
            except Exception as e:
                print("Failed sending metrics to backend", e)

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
            print(f"Received event {event}")
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