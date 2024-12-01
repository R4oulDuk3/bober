import asyncio

from core.exporter_side_car import SideCarExporter, AsyncSubscriber


async def main():
    metrics_collector = SideCarExporter()
    subscriber = AsyncSubscriber(metrics_collector, listen_address="tcp://127.0.0.1:5555")
    try:
        await subscriber.run()
    except KeyboardInterrupt:
        print("Shutting down...")


if __name__ == "__main__":
    asyncio.run(main())