import asyncio

from analytics.analytics_client import produce_machine_iot_client
from core.control_loop import ControlLoop
from implementations.advanced_motor_controller import AdvancedMotorController
from implementations.infra_red_sensor_controller import IRSensorController
from implementations.in_memory_observability_controller import InMemoryObservabilityController
from implementations.queued_observability_controller import QueuedObservabilityController
from implementations.simple_motor_controller import SimpleMotorController
from infrastructure.async_publisher import AsyncPublisher
from infrastructure.config_loader import ConfigLoader


async def main():
    #
    # analytics_client = produce_machine_iot_client()
    #
    # control_loop = ControlLoop(
    #     motor=AdvancedMotorController(),
    #     sensor=IRSensorController(),
    #     observability=InMemoryObservabilityController(
    #         analytics_client=analytics_client
    #     ),
    #     delay_millis=100,
    #     config_loader=ConfigLoader(
    #         config_path="config.json"
    #     )
    # )

    async_publisher = AsyncPublisher(
        publish_address="tcp://127.0.0.1:5555"
    )
    await async_publisher.connect()
    control_loop = ControlLoop(
        motor=AdvancedMotorController(),
        sensor=IRSensorController(),
        observability=QueuedObservabilityController(
            publisher=async_publisher
        ),
        delay_millis=100,
        config_loader=ConfigLoader(
            config_path="config.json"
        )
    )
    try:
        await control_loop.run()
    except:
        await control_loop.stop()

if __name__ == "__main__":
    asyncio.run(main())