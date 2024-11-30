# src/core/control_loop.py
import time

from analytics.analytics_client import produce_machine_iot_client
from enums import MachineStatus
from implementations.motor_controller import MotorController
from implementations.observability_controller import ObservabilityController
from implementations.sensor_controller import SensorController
from interfaces.motor_interface import IMotorController
from interfaces.sensor_interface  import ISensorController
from interfaces.observability_interface import IObservabilityController
import asyncio
import datetime

class ControlLoop:
    def __init__(self,
                 motor: IMotorController,
                 sensor: ISensorController,
                 observability: IObservabilityController):
        self.motor = motor
        self.sensor = sensor
        self.observability = observability
        self.box_count = 0
        self.is_running = False

    async def run(self) -> None:
        self.is_running = True
        self.motor.start_motor()
        #self.sensor.start_sensor1()
        #self.sensor.start_sensor2()

        last_sensor1_state = False
        print("Starting loop")
        while self.is_running:
            try:
                current_sensor1_state = self.sensor.is_sensor1_triggered()

                # Detect rising edge on sensor 1 (new box detected)
                if current_sensor1_state and not last_sensor1_state and not ( current_sensor1_state is False):
                    self.box_count += 1

                last_sensor1_state = current_sensor1_state
                await self.observability.observe_machine_state(
                    box_count=self.box_count,
                    status=MachineStatus.RUNNING,
                    machine_speed=5
                )
                time.sleep(1)  # Small delay to prevent CPU hogging
                # print("Running...")
            except Exception as e:
                await self.observability.observe_machine_state(
                    box_count=self.box_count,
                    status=MachineStatus.ERROR,
                    machine_speed=5
                )

                self.stop()
                raise

    async def stop(self) -> None:
        self.is_running = False
        self.motor.stop_motor()
        self.sensor.stop_sensor1()
        self.sensor.stop_sensor2()
        await self.observability.observe_machine_state(
            box_count=self.box_count,
            status=MachineStatus.STOPPED,
            machine_speed=0
        )


async def main():

    analytics_client = produce_machine_iot_client()

    control_loop = ControlLoop(
        motor=MotorController(),
        sensor=SensorController(),
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
