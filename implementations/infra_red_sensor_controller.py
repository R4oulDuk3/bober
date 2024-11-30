from abc import ABC, abstractmethod
from gpiozero import DigitalInputDevice
import time

from interfaces.sensor_interface import ISensorController


class IRSensorController(ISensorController):
    def __init__(self, pin: int = 22):
        self.ir_sensor = DigitalInputDevice(pin)

    def is_box_visible(self) -> bool:
        return not self.ir_sensor.value


# Example usage:
if __name__ == "__main__":
    sensor = IRSensorController()
    print("IR Sensor is running. Press CTRL+C to exit")

    try:
        was_visible = sensor.is_box_visible()  # Store initial state
        while True:
            is_visible = sensor.is_box_visible()
            if is_visible != was_visible:  # State has changed
                if is_visible:
                    print("Box is now visible!")
                else:
                    print("Box is no longer visible!")
                was_visible = is_visible
            time.sleep(0.1)  # Small delay to prevent CPU overuse

    except KeyboardInterrupt:
        print("\nExiting program")