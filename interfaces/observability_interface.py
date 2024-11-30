
# src/interfaces/observability_interface.py
from abc import ABC, abstractmethod
from typing import Any

class IObservabilityController(ABC):
    @abstractmethod
    def log_machine_status(self, status: str) -> None:
        pass

    @abstractmethod
    def log_box_count(self, count: int) -> None:
        pass

    @abstractmethod
    def log_track_speed(self, speed: float) -> None:
        pass

    @abstractmethod
    def start_logging(self) -> None:
        pass

    @abstractmethod
    def stop_logging(self) -> None:
        pass
