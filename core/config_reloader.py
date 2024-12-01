import asyncio
import aiohttp
import logging
from datetime import datetime

from infrastructure.config_loader import ConfigLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HttpConfigReloader:
    def __init__(self, config_loader: ConfigLoader, endpoint_url: str, interval: float = 2.0):
        """
        Initialize ConfigReloader

        Args:
            config_loader: Instance of ConfigLoader class
            endpoint_url: URL to fetch JSON from
            interval: Sleep interval between requests in seconds
        """
        self.config_loader = config_loader
        self.endpoint_url = endpoint_url
        self.interval = interval
        self._running = False

    async def run(self):
        """Start the config reloader loop"""
        self._running = True
        async with aiohttp.ClientSession() as session:
            while self._running:
                try:
                    # Fetch data from endpoint
                    async with session.get(self.endpoint_url) as response:
                        if response.status == 200:
                            data = await response.json()

                            # Save the fetched data to config
                            self.config_loader.save_config(data)
                            logger.info(f"Config updated at {datetime.now()}")
                        else:
                            logger.error(f"Failed to fetch config: HTTP {response.status}")

                except aiohttp.ClientError as e:
                    logger.error(f"Network error while fetching config: {e}")
                except Exception as e:
                    logger.error(f"Unexpected error while updating config: {e}")

                # Wait before next update
                await asyncio.sleep(self.interval)

    def stop(self):
        """Stop the config reloader loop"""
        self._running = False
        logger.info("Config reloader stopped")


async def main():
    config_loader = ConfigLoader("test-config.json")
    reloader = HttpConfigReloader(config_loader, "http://10.0.4.62:80/api/v1/config")

    try:
        await reloader.run()
    except KeyboardInterrupt:
        reloader.stop()


if __name__ == "__main__":
    asyncio.run(main())