
# src/interfaces/sensor_interface.py
from abc import ABC, abstractmethod

class ISensorController(ABC):
    @abstractmethod
    def start_sensor1(self) -> None:
        pass

    @abstractmethod
    def stop_sensor1(self) -> None:
        pass

    @abstractmethod
    def start_sensor2(self) -> None:
        pass

    @abstractmethod
    def stop_sensor2(self) -> None:
        pass

    @abstractmethod
    def is_sensor1_triggered(self) -> bool:
        pass

    @abstractmethod
    def is_sensor2_triggered(self) -> bool:
        pass

    @abstractmethod
    def get_status(self) -> dict:
        """Get current sensor status"""
        pass