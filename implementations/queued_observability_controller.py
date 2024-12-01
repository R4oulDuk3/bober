# src/implementations/in_memory_observability_controller.py
from enum import Enum

from analytics.analytics_client import MachineIoTClient
from analytics.metric import MetricsRegistry
from enums import MachineStatus
from infrastructure.async_publisher import AsyncPublisher
from infrastructure.boblogger import BobLogger
from interfaces.observability_interface import IObservabilityController
from datetime import datetime

class QueuedObservabilityController(IObservabilityController):



    async def flush(self):
        logs = self.logger.get_logs()[:]
        self.logger.clear()

        if len(logs) > 0:
            await self.publisher.flush_logs(logs)

        await self.publisher.flush_metrics(self.metrics_registry)


    async def observe_system_info(self):
        await self.publisher.publish_system_info()
        self.metrics_registry.observe_system_metrics()


    async def observe_machine_status_changed(self, box_count: int, machine_speed: int, status: MachineStatus, event: str) -> None:
        await self.publisher.publish_event(
            event_name=event,
            data={
                "totaloutputunitcount": box_count,
                "machinespeed": machine_speed,
            }
        )
        await self.observe_is_on(machine_speed)

    async def observe_running_state(self, box_count: int, machine_speed: float) -> None:
        self.logger.info(f"Current state: box_count={box_count}, machine_speed={machine_speed}")
        await self.publisher.publish_telemetry(data={
            "totaloutputunitcount": box_count,
            "machinespeed": machine_speed,
        })
        await self.observe_is_on(machine_speed)

    async def observe_is_on(self, machine_speed):
        if machine_speed == 0:
            self.metrics_registry.set_gauge("is_running", 0)
        else:
            self.metrics_registry.set_gauge("is_running", 1)

    def __init__(self, publisher: AsyncPublisher, logger: BobLogger):
        self.publisher = publisher
        self.metrics_registry = MetricsRegistry()
        self.logger = logger

