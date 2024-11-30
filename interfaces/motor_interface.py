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
        """Increase motor speed"""
        pass

    @abstractmethod
    def slow_down(self) -> None:
        """Decrease motor speed"""
        pass

    @abstractmethod
    def get_status(self) -> dict:
        """Get current motor status"""
        pass
