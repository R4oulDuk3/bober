import json
import os
from datetime import datetime, timedelta


class ConfigLoader:
    def __init__(self, config_path: str):
        self._config_path = config_path
        self._config = {}
        self._last_reload_time = None
        self._reload_interval = timedelta(seconds=3)
        self.reload_config()

    def should_reload(self) -> bool:
        """Check if config needs to be reloaded and reload if necessary."""
        if self._last_reload_time is None:
            self.reload_config()
            return True

        time_since_reload = datetime.now() - self._last_reload_time
        if time_since_reload > self._reload_interval:
            self.reload_config()
            return True

        return False

    def reload_config(self) -> None:
        """Reload configuration from file and update timestamp."""
        if not os.path.exists(self._config_path):
            raise FileNotFoundError(f"Config file not found at {self._config_path}")

        with open(self._config_path, 'r') as file:
            self._config = json.load(file)
            self._last_reload_time = datetime.now()

    @property
    def last_reload_time(self) -> datetime:
        """Get the timestamp of the last config reload."""
        return self._last_reload_time

    @property
    def config(self) -> dict:
        """Get the current configuration."""
        return self._config.copy()

    def get_value(self, key: str, default=None):
        """Get a specific configuration value."""
        return self._config.get(key, default)

    def is_power_on(self) -> bool:
        """Check if power is on."""
        return self.get_value('power') == 'on'

    def get_speed(self) -> int:
        """Get the speed value."""
        return int(self.get_value('speed', 0))

    def save_config(self, config: dict) -> None:
        """Save new configuration to file."""
        with open(self._config_path, 'w') as file:
            json.dump(config, file, indent=2)
        self.reload_config()