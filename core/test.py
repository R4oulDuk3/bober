import asyncio
import aiozmq
import zmq
import json
from datetime import datetime

from infrastructure.async_publisher import AsyncPublisher


async def main():
    publisher = AsyncPublisher(publish_address="tcp://127.0.0.1:5555")
    await publisher.connect()

    try:
        # Publish some example telemetry
        await publisher.publish_telemetry({
            "cpu_usage": 75.5,
            "memory_usage": 8192,
            "disk_space": 512000
        })

        await asyncio.sleep(1)  # Wait a bit between messages

        # Publish some example events
        await publisher.publish_event("user_login", {
            "user_id": "12345",
            "login_time": datetime.now().isoformat(),
            "success": True
        })

        await asyncio.sleep(1)

        await publisher.publish_event("api_call", {
            "endpoint": "/api/v1/users",
            "method": "POST",
            "response_time": 145.2
        })

    except KeyboardInterrupt:
        print("Shutting down publisher...")
    finally:
        publisher.pub.close()

if __name__ == "__main__":
    asyncio.run(main())