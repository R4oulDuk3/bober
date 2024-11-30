# src/core/control_loop.py
import time

from analytics.analytics_client import produce_machine_iot_client
from enums import MachineStatus
from implementations.mock_motor_controller import MockMotorController
from implementations.observability_controller import ObservabilityController
from implementations.mock_sensor_controller import MockSensorController
from interfaces.motor_interface import IMotorController
from interfaces.sensor_interface  import ISensorController
from interfaces.observability_interface import IObservabilityController
import asyncio
import datetime

class ControlLoop:
    def __init__(self,
                 motor: IMotorController,
                 sensor: ISensorController,
                 observability: IObservabilityController,
                 delay_millis: float):
        self.motor = motor
        self.sensor = sensor
        self.observability = observability
        self.box_count = 0
        self.is_running = False
        self.machine_speed = 1
        self.delay_millis = delay_millis

    async def run(self) -> None:
        self.is_running = True
        self.motor.start_motor()
        await self.observability.observe_machine_status_changed(
            box_count=self.box_count,
            machine_speed=self.machine_speed,
            event="Process Started",
            status=MachineStatus.RUNNING
        )
        box_visible_in_previous_cycle = False
        print("Starting loop")
        while self.is_running:
            try:
                self.machine_speed += 1
                box_visible_currently = self.sensor.is_box_visible()

                # Detect rising edge on sensor 1 (new box detected)
                if not box_visible_in_previous_cycle and box_visible_currently:
                    self.box_count += 1

                box_visible_in_previous_cycle = box_visible_currently
                await self.observability.observe_running_state(
                    box_count=self.box_count,
                    machine_speed=self.machine_speed
                )
                time.sleep(self.delay_millis)
            except Exception as e:
                await self.observability.observe_machine_status_changed(
                    box_count=self.box_count,
                    machine_speed=self.machine_speed,
                    event="Error occurred",
                    status=MachineStatus.ERROR
                )
                print(f"Error occurred {e}")

                await self.stop()
                raise

    async def stop(self) -> None:
        self.is_running = False
        self.motor.stop_motor()

        await self.observability.observe_machine_status_changed(
            box_count=self.box_count,
            machine_speed=self.machine_speed,
            event="Process Stopped",
            status=MachineStatus.STOPPED
        )


async def main():

    analytics_client = produce_machine_iot_client()

    control_loop = ControlLoop(
        motor=MockMotorController(),
        sensor=MockSensorController(),
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
