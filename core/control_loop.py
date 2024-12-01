# src/core/control_loop.py
import asyncio
import datetime
import time

# from analytics.analytics_client import produce_machine_iot_client
from enums import MachineStatus
from implementations.mock_motor_controller import MockMotorController
from implementations.mock_sensor_controller import MockSensorController
from implementations.queued_observability_controller import QueuedObservabilityController
from infrastructure import config_loader
from infrastructure.async_publisher import AsyncPublisher
from infrastructure.config_loader import ConfigLoader
from interfaces.motor_interface import IMotorController
from interfaces.observability_interface import IObservabilityController
from interfaces.sensor_interface import ISensorController


class ControlLoop:
    def __init__(self,
                 motor: IMotorController,
                 sensor: ISensorController,
                 observability: IObservabilityController,
                 config_loader: ConfigLoader,
                 delay_millis: float):
        self.motor = motor
        self.sensor = sensor
        self.observability = observability
        self.box_count = 0
        self.is_running = False
        self.desired_speed = 10
        self.config_loader = config_loader
        self.delay_millis = delay_millis
        self.last_telemetry_timestamp = 0
        self.telemetry_send_threshold = 10

    def try_reload_config(self):
        if self.config_loader.should_reload():
            self.config_loader.reload_config()
            print(f"Reloaded config {self.config_loader.config}")

        self.desired_speed = self.config_loader.get_speed()
        # print(f"Updated desired speed to {self.desired_speed}")

    def manage_speed(self):
        machine_speed = self.motor.get_speed()
        if machine_speed == self.desired_speed:
            return
        elif machine_speed > self.desired_speed:
            print(f"Desired speed is lesser then machine speed, slowing down... [machine speed: {machine_speed}, desired_speed: {self.desired_speed}]")
            self.motor.slow_down()
        else:
            self.motor.speed_up()
            print(f"Desired speed is greater then machine speed, speeding up... [machine speed: {machine_speed}, desired_speed: {self.desired_speed}]")


    async def try_send_telemetry(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        time_since_last_send = now.timestamp() - self.last_telemetry_timestamp

        if time_since_last_send > self.telemetry_send_threshold:
            try:
                await self.observability.observe_running_state(
                    box_count=self.box_count,
                    machine_speed=self.motor.get_speed()
                )
                self.last_telemetry_timestamp = now.timestamp()
                return True
            except Exception as e:
                print(f"Error sending telemetry: {e}")
                return False


    async def run(self) -> None:
        self.is_running = True
        self.motor.start_motor()
        await self.observability.observe_machine_status_changed(
            box_count=self.box_count,
            machine_speed=self.motor.get_speed(),
            event="Process Started",
            status=MachineStatus.RUNNING
        )
        box_visible_in_previous_cycle = False
        print("Starting loop")
        while self.is_running:
            try:
                self.try_reload_config()
                self.manage_speed()
                box_visible_currently = self.sensor.is_box_visible()

                # Detect rising edge on sensor 1 (new box detected)
                if not box_visible_in_previous_cycle and box_visible_currently:
                    self.box_count += 1
                    print("New box appeared")

                box_visible_in_previous_cycle = box_visible_currently


                await self.try_send_telemetry()

                time.sleep(self.delay_millis / 1000)
            except Exception as e:
                await self.observability.observe_machine_status_changed(
                    box_count=self.box_count,
                    machine_speed=self.motor.get_speed(),
                    event="Error occurred",
                    status=MachineStatus.ERROR
                )
                print(f"Error occurred {e}")
                await self.stop()


    async def stop(self) -> None:
        self.is_running = False
        self.motor.stop_motor()

        await self.observability.observe_machine_status_changed(
            box_count=self.box_count,
            machine_speed=self.motor.get_speed(),
            event="Process Stopped",
            status=MachineStatus.STOPPED
        )


async def main():

    # analytics_client = produce_machine_iot_client()
    async_publisher = AsyncPublisher(
        publish_address="tcp://127.0.0.1:5555"
    )

    await async_publisher.connect()
    control_loop = ControlLoop(
        motor=MockMotorController(),
        sensor=MockSensorController(),
        observability=QueuedObservabilityController(
            publisher=async_publisher
        ),
        delay_millis=500,
        config_loader=ConfigLoader(config_path="../config.json")
    )

    try:
        await control_loop.run()
    except:
        await control_loop.stop()

if __name__ == "__main__":
    asyncio.run(main())
