# src/implementations/logging_controller.py
from ..interfaces.logging_interface import ILoggingController
from datetime import datetime


class LoggingController(ILoggingController):
    is_logging: bool

    def __init__(self):
        self.is_logging = False

    def log_machine_status(self, status: str) -> None:
        if not self.is_logging:
            return
        print(f"[{datetime.now()}] Machine Status: {status}")

    def log_box_count(self, count: int) -> None:
        if not self.is_logging:
            return
        print(f"[{datetime.now()}] Box Count: {count}")

    def log_track_speed(self, speed: float) -> None:
        if not self.is_logging:
            return
        print(f"[{datetime.now()}] Track Speed: {speed}")

    def start_logging(self) -> None:
        self.is_logging = True
        self.log_machine_status("Logging Started")

    def stop_logging(self) -> None:
        self.log_machine_status("Logging Stopped")
        self.is_logging = False