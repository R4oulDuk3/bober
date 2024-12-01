# src/interfaces/motor_interface.py
from abc import ABC, abstractmethod

class IMotorController(ABC):
    @abstractmethod
    def start_motor(self) -> None:
        """Start motor at default speed"""
        pass

    @abstractmethod
    def stop_motor(self) -> None:
        """Stop motor completely"""
        pass

    @abstractmethod
    def speed_up(self) -> None:
        """Stop motor completely"""
        pass

    def slow_down(self) -> None:
        pass

    @abstractmethod
    def get_speed(self) -> int:
        pass

