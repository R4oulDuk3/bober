import asyncio

from core.config_reloader import HttpConfigReloader
from infrastructure.config_loader import ConfigLoader


async def main():
    config_loader = ConfigLoader("config.json")
    reloader = HttpConfigReloader(config_loader, "http://10.0.4.62:80/api/v1/config")

    try:
        await reloader.run()
    except KeyboardInterrupt:
        reloader.stop()


if __name__ == "__main__":
    asyncio.run(main())