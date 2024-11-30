# enums.py
from enum import Enum

class MotorDirection(Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2

class MachineStatus(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    WARNING = "warning"
    ERROR = "error"