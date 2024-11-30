# src/implementations/sensor_controller.py
from ..interfaces.sensor_interface import ISensorController


class SensorController(ISensorController):
    sensor1_active: bool
    sensor2_active: bool

    def __init__(self):
        self.sensor1_active = False
        self.sensor2_active = False

    def start_sensor1(self) -> None:
        self.sensor1_active = True

    def stop_sensor1(self) -> None:
        self.sensor1_active = False

    def start_sensor2(self) -> None:
        self.sensor2_active = True

    def stop_sensor2(self) -> None:
        self.sensor2_active = False

    def is_sensor1_triggered(self) -> bool:
        if not self.sensor1_active:
            return False
        return False  # Replace with actual sensor reading

    def is_sensor2_triggered(self) -> bool:
        if not self.sensor2_active:
            return False
        return False  # Replace with actual sensor reading

    def get_status(self) -> dict:
        return {
            "sensor1_active": self.sensor1_active,
            "sensor2_active": self.sensor2_active,
            "sensor1_triggered": self.is_sensor1_triggered() if self.sensor1_active else None,
            "sensor2_triggered": self.is_sensor2_triggered() if self.sensor2_active else None
        }