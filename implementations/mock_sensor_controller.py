# src/implementations/mock_sensor_controller.py
from interfaces.sensor_interface import ISensorController


class MockSensorController(ISensorController):

    def __init__(self):
        self.counter = 0
        self.switch_point = 3
        self.is_visible = False

    def is_box_visible(self) -> bool:
        self.counter += 1
        if self.counter  == self.switch_point:
            self.is_visible = not self.is_visible
            self.counter = 0

        print(f"mock sensor state {self.is_visible} point {self.switch_point} counter {self.counter} ")

        return self.is_visible
