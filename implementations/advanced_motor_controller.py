from time import sleep

import RPi.GPIO as GPIO

from interfaces.motor_interface import IMotorController

class GradualMotor:
    def __init__(self, pin, frequency, modifier ):
        self._current_speed = 0
        self._speed_modifier = modifier
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self._motor = GPIO.PWM(pin, frequency)

    def speed_up(self ) -> bool:
        if self._current_speed<14 and self._current_speed> 0:
            self._current_speed += self._speed_modifier
        else:
            self.current_speed = 10
        self._motor.ChangeDutyCycle(self._current_speed)

    def speed_down(self ) -> bool:
        if self._current_speed>10:
            self._current_speed -= self._speed_modifier

        else:
            self._current_speed = 0
        self._motor.ChangeDutyCycle(self._current_speed)

    def get_current_speed(self) -> int:
        return self._current_speed

    def start(self):
        self._current_speed = 10
        self._motor.start(self._current_speed)

    def stop(self) -> None:
        self.current_speed = 0
        self._motor.ChangeDutyCycle(self._current_speed)
        """Stop the motor."""

    def cleanup(self) -> None:
        """Clean up GPIO resources."""
        self._motor.stop()
        print("Motor cleanup completed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()


class AdvancedMotorController(IMotorController):

    def __init__(self):
        self.currentSpeed = 0;
        self.isRunning = False
        self.motor = GradualMotor(18, 50, 2)


    def start(self):
        if not self.isRunning:
            self.isRunning = True
            self.motor.start()

    def speedUp(self):
        if self.isRunning:
            self.motor.speed_up()

    def speedDown(self):
        if self.isRunning:
            self.motor.speed_down()

    def stop(self):
        if self.isRunning:
            self.isRunning = False
            self.motor.stop()