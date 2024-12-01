import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import List


class Severity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"


@dataclass
class LogMessage:
    timestamp: datetime
    message: str
    severity: Severity

    def __str__(self) -> str:
        return f"[{self.timestamp.isoformat()}] {self.severity.value}: {self.message}"

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.timestamp(),
            "message": self.message,
            "severity": self.severity.value,
        }


class BobLogger:
    def __init__(self):
        self.messages: List[LogMessage] = []

    def _log(self, message: str, severity: Severity) -> None:
        log_message = LogMessage(
            timestamp=datetime.now(timezone.utc),
            message=message,
            severity=severity
        )
        print(str(log_message))
        self.messages.append(log_message)

    def info(self, message: str) -> None:
        self._log(message, Severity.INFO)

    def warning(self, message: str) -> None:
        self._log(message, Severity.WARNING)

    def error(self, message: str, exc: Exception = None):
        stack_trace = None
        if exc:
            stack_trace = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        log_message = LogMessage(
            message=message + " " + stack_trace,
            severity=Severity.ERROR,
            timestamp=datetime.now(timezone.utc),
        )
        print(str(log_message))
        self.messages.append(log_message)


    def debug(self, message: str) -> None:
        self._log(message, Severity.DEBUG)

    def get_logs(self) -> List[LogMessage]:
        return self.messages

    def clear(self) -> None:
        self.messages.clear()




