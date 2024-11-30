
# src/interfaces/sensor_interface.py
from abc import ABC, abstractmethod

class ISensorController(ABC):
    @abstractmethod
    def is_box_visible(self) -> bool:
        pass
