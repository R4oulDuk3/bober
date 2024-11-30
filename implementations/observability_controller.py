# src/implementations/observability_controller.py
from enum import Enum

from analytics.analytics_client import MachineIoTClient
from enums import MachineStatus
from interfaces.observability_interface import IObservabilityController
from datetime import datetime

class MachineEvent(Enum):
    POWER_ON = 0
    RUNNING = 2
    PRODUCING = 3
    POWER_OFF = 4


def map_status_to_event(status: MachineStatus) -> MachineEvent:
    if status == MachineStatus.RUNNING:
        return MachineEvent.RUNNING
    elif status == MachineStatus.STOPPED:
        return MachineEvent.POWER_OFF
    else:  # WARNING or ERROR
        return MachineEvent.POWER_OFF


class ObservabilityController(IObservabilityController):

    def map_machine_status_to_machine_event(self):
        pass

    async def observe_machine_status_changed(self, box_count: int, machine_speed: int, status: MachineStatus, event: str) -> None:
        await self.analytics_client.send_machine_event(
            total_output_unit_count=box_count,
            machine_speed=machine_speed,
            event_type=event,
            job_id="123"

        )

    async def observe_running_state(self, box_count: int, machine_speed: int) -> None:
        print(f"Current state: box_count={box_count}, machine_speed={machine_speed}")
        await self.analytics_client.send_telemetry(
            total_output_unit_count=box_count,
            machine_speed=machine_speed
        )


    def __init__(self, analytics_client: MachineIoTClient):
        self.analytics_client = analytics_client

