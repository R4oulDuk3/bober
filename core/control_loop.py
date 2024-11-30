# src/core/control_loop.py
import time
from ..interfaces.motor_interface import IMotorController
from ..interfaces.sensor_interface  import ISensorController
from ..interfaces.observability_interface import IObservabilityController


class ControlLoop:
    def __init__(self,
                 motor: IMotorController,
                 sensor: ISensorController,
                 logger: IObservabilityController):
        self.motor = motor
        self.sensor = sensor
        self.logger = logger
        self.box_count = 0
        self.is_running = False

    def run(self) -> None:
        self.is_running = True
        self.motor.start_motor()
        #self.sensor.start_sensor1()
        #self.sensor.start_sensor2()

        last_sensor1_state = False

        while self.is_running:
            try:
                current_sensor1_state = self.sensor.is_sensor1_triggered()

                # Detect rising edge on sensor 1 (new box detected)
                if current_sensor1_state and not last_sensor1_state and not ( current_sensor1_state is False):
                    self.box_count += 1
                    self.logger.log_box_count(self.box_count)

                last_sensor1_state = current_sensor1_state
                # observe_state
                time.sleep(0.01)  # Small delay to prevent CPU hogging

            except Exception as e:
                self.logger.log_machine_status(f"Error: {str(e)}")
                self.stop()
                raise

    def stop(self) -> None:
        self.is_running = False
        self.motor.stop_motor()
        self.sensor.stop_sensor1()
        self.sensor.stop_sensor2()
        self.logger.log_machine_status("Stopped")

    def get_status(self) -> dict:
        return {
            "box_count": self.box_count,
            "is_running": self.is_running,
            "motor_status": self.motor.get_status(),
            "sensor_status": self.sensor.get_status()
        }

    def log (self) -> None:
        # OVDE MOZDA NEKI THREAD DA PUSTIMO DA SE VRTI I ROKA PODATKE

        motor_status = self.motor.get_status()
        self.logger.log_track_speed(motor_status["current_speed"])
