import asyncio

from analytics.analytics_client import produce_machine_iot_client
from core.control_loop import ControlLoop
from implementations.infra_red_sensor_controller import IRSensorController
from implementations.mock_motor_controller import MockMotorController
from implementations.observability_controller import ObservabilityController


async def main():

    analytics_client = produce_machine_iot_client()

    control_loop = ControlLoop(
        motor=MockMotorController(),
        sensor=IRSensorController(),
        observability=ObservabilityController(
            analytics_client=analytics_client
        ),
    )
    try:
        await control_loop.run()
    except:
        await control_loop.stop()

if __name__ == "__main__":
    asyncio.run(main())