# src/core/control_loop.py
import asyncio
import datetime
import time
import traceback

# from analytics.analytics_client import produce_machine_iot_client
from enums import MachineStatus
from implementations.mock_motor_controller import MockMotorController
from implementations.mock_sensor_controller import MockSensorController
from implementations.queued_observability_controller import QueuedObservabilityController
from infrastructure import config_loader
from infrastructure.async_publisher import AsyncPublisher
from infrastructure.config_loader import ConfigLoader
from infrastructure.boblogger import BobLogger
from interfaces.motor_interface import IMotorController
from interfaces.observability_interface import IObservabilityController
from interfaces.sensor_interface import ISensorController


class ControlLoop:
    def __init__(self,
                 motor: IMotorController,
                 sensor: ISensorController,
                 observability: IObservabilityController,
                 config_loader: ConfigLoader,
                 logger: BobLogger,
                 delay_millis: float):
        self.motor = motor
        self.logger = logger
        self.sensor = sensor
        self.observability = observability
        self.box_count = 0
        self.is_on = True
        self.is_running = False
        self.desired_speed = 10
        self.config_loader = config_loader
        self.delay_millis = delay_millis
        self.last_telemetry_timestamp = 0
        self.telemetry_send_threshold = 10

    async def try_reload_config(self):
        if self.config_loader.should_reload():
            self.config_loader.reload_config()
            await self.observability.observe_system_info()
            print(f"Reloaded config {self.config_loader.config}")

        self.desired_speed = self.config_loader.get_speed()
        new_power_value = self.config_loader.is_power_on()


        if new_power_value != self.is_on:
            print(f"Machine power switched! [Previous {self.is_on}, current {new_power_value}]")
            self.is_on = new_power_value

        # print(f"Updated desired speed to {self.desired_speed}")

    async def handle_power_switch(self):

        if self.is_on and not self.motor.is_running():
            self.logger.info("Turning the motor on!")
            self.motor.start_motor()
            await self.observability.observe_machine_status_changed(
                box_count=self.box_count,
                machine_speed=self.motor.get_speed(),
                event="Started",
                status=MachineStatus.RUNNING
            )

        elif not self.is_on and self.motor.is_running():
            self.logger.info("Turning the motor off!")
            self.motor.stop_motor()
            await self.observability.observe_machine_status_changed(
                box_count=self.box_count,
                machine_speed=self.motor.get_speed(),
                event="Stopped",
                status=MachineStatus.STOPPED
            )


    def manage_speed(self):

        if not self.is_on:
            return

        machine_speed = self.motor.get_speed()
        if machine_speed == self.desired_speed:
            return
        elif machine_speed > self.desired_speed:
            self.logger.info(f"Desired speed is lesser then machine speed, slowing down... [machine speed: {machine_speed}, desired_speed: {self.desired_speed}]")
            self.motor.slow_down()
        else:
            self.motor.speed_up()
            self.logger.info(f"Desired speed is greater then machine speed, speeding up... [machine speed: {machine_speed}, desired_speed: {self.desired_speed}]")


    async def try_send_telemetry(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        time_since_last_send = now.timestamp() - self.last_telemetry_timestamp

        if time_since_last_send > self.telemetry_send_threshold:
            try:
                speed = self.motor.get_speed()
                self.logger.info(f"Send telemetry [box_count {self.box_count}, machine_speed {speed}]")
                await self.observability.observe_running_state(
                    box_count=self.box_count,
                    machine_speed=speed
                )

                self.last_telemetry_timestamp = now.timestamp()
                return True
            except Exception as e:
                self.logger.error(f"Error sending telemetry", e)
                return False


    async def run(self) -> None:
        self.is_running = True
        self.motor.start_motor()
        await self.observability.observe_machine_status_changed(
            box_count=self.box_count,
            machine_speed=self.motor.get_speed(),
            event="Running",
            status=MachineStatus.RUNNING
        )

        box_visible_in_previous_cycle = False
        self.logger.debug("Starting loop")
        while self.is_running:
            try:


                await self.try_reload_config()
                await self.handle_power_switch()

                self.manage_speed()
                box_visible_currently = self.sensor.is_box_visible()

                # Detect rising edge on sensor 1 (new box detected)
                if not box_visible_in_previous_cycle and box_visible_currently:
                    self.box_count += 1
                    self.logger.debug("New box appeared")

                box_visible_in_previous_cycle = box_visible_currently

                await self.try_send_telemetry()

                await self.observability.flush()
                time.sleep(self.delay_millis / 1000)
            except Exception as e:
                await self.observability.observe_machine_status_changed(
                    box_count=self.box_count,
                    machine_speed=self.motor.get_speed(),
                    event="ErrorOccurred",
                    status=MachineStatus.ERROR
                )
                print(f"Error! {e}")
                print(traceback.format_exc())
                # self.logger.error(f"Error occurred {e}")
                await self.stop()


    async def stop(self) -> None:
        self.is_running = False
        self.motor.stop_motor()

        await self.observability.observe_machine_status_changed(
            box_count=self.box_count,
            machine_speed=self.motor.get_speed(),
            event="Stopped",
            status=MachineStatus.STOPPED
        )


async def main():

    # analytics_client = produce_machine_iot_client()
    async_publisher = AsyncPublisher(
        publish_address="tcp://127.0.0.1:5555"
    )
    logger = BobLogger()
    await async_publisher.connect()
    control_loop = ControlLoop(
        motor=MockMotorController(),
        sensor=MockSensorController(),
        observability=QueuedObservabilityController(
            publisher=async_publisher,
            logger=logger
        ),
        delay_millis=500,
        config_loader=ConfigLoader(config_path="../config.json"),
        logger=logger
    )

    try:
        await control_loop.run()
    except:
        await control_loop.stop()

if __name__ == "__main__":
    asyncio.run(main())
