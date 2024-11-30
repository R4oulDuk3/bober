from ..interfaces.motor_interface import IMotorController

class MotorController(IMotorController):

    default_speed: float
    current_speed: float
    is_running: bool

    def __init__(self):
        self.current_speed = 0.0
        self.default_speed = 50.0
        self.is_running = False

    def start_motor(self) -> None:
        self.is_running = True

    def stop_motor(self) -> None:
        self.is_running = False

    def speed_up(self) -> None:
        self.speed_up()

    def slow_down(self) -> None:
        self.slow_down()

    def get_status(self) -> dict:
        return {
            "is_running": self.is_running,
            "current_speed": self.current_speed
        }