
# src/interfaces/observability_interface.py
from abc import ABC, abstractmethod
from typing import Any

from enums import MachineStatus


class IObservabilityController(ABC):

    @abstractmethod
    async def flush(self):
        pass

    @abstractmethod
    async def observe_running_state(self, box_count: int, machine_speed: float) -> None:
        pass

    @abstractmethod
    async def observe_machine_status_changed(self, box_count: int, machine_speed: int, status: MachineStatus, event: str) -> None:
        pass

    @abstractmethod
    async def observe_system_info(self):
        pass