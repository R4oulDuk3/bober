# src/implementations/in_memory_observability_controller.py
from enum import Enum

from analytics.analytics_client import MachineIoTClient
from enums import MachineStatus
from infrastructure.async_publisher import AsyncPublisher
from interfaces.observability_interface import IObservabilityController
from datetime import datetime

class QueuedObservabilityController(IObservabilityController):


    async def observe_machine_status_changed(self, box_count: int, machine_speed: int, status: MachineStatus, event: str) -> None:
        await self.publisher.publish_event(
            event_name=event,
            data={
                "total_output_unit_count": box_count,
                "machine_speed": machine_speed,
            }
        )

    async def observe_running_state(self, box_count: int, machine_speed: float) -> None:
        print(f"Current state: box_count={box_count}, machine_speed={machine_speed}")
        await self.publisher.publish_telemetry(data={
            "totaloutputunitcount": box_count,
            "machinespeed": machine_speed,
        })


    def __init__(self, publisher: AsyncPublisher):
        self.publisher = publisher

