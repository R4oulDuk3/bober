import asyncio

from analytics.analytics_client import produce_machine_iot_client
from core.control_loop import ControlLoop
from implementations.infra_red_sensor_controller import IRSensorController
from implementations.in_memory_observability_controller import InMemoryObservabilityController
from implementations.simple_motor_controller import SimpleMotorController


async def main():

    analytics_client = produce_machine_iot_client()

    control_loop = ControlLoop(
        motor=SimpleMotorController(),
        sensor=IRSensorController(),
        observability=InMemoryObservabilityController(
            analytics_client=analytics_client
        ),
        delay_millis=100
    )
    try:
        await control_loop.run()
    except:
        await control_loop.stop()

if __name__ == "__main__":
    asyncio.run(main())