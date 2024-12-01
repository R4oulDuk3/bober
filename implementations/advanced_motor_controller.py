from time import sleep

import RPi.GPIO as GPIO

from interfaces.motor_interface import IMotorController

class AdvancedMotor:
    def __init__(self, pin, frequency, modifier = 1):
        self._current_speed = 0
        self._speed_modifier = modifier
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self._motor = GPIO.PWM(pin, frequency)

    def speed_up(self ):
        if 14 > self._current_speed > 0:
            self._current_speed += self._speed_modifier
            self._motor.ChangeDutyCycle(self._current_speed)


    def speed_down(self ):
        if self._current_speed>10:
            self._current_speed -= self._speed_modifier
            self._motor.ChangeDutyCycle(self._current_speed)

    def get_current_speed(self) -> int:
        return self._current_speed

    def start(self):
        self._current_speed = 10
        self._motor.start(self._current_speed)

    def stop(self) -> None:
        self._current_speed = 0
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

    def get_speed(self) -> int:
        return self.motor.get_current_speed()

    def slow_down(self) -> None:
        if self.isRunning:
            self.motor.speed_down()

    def speed_up(self) -> None:
        if self.isRunning:
            self.motor.speed_up()

    def stop_motor(self) -> None:
        if self.isRunning:
            self.isRunning = False
            self.motor.stop()

    def start_motor(self) -> None:
        if not self.isRunning:
            self.isRunning = True
            self.motor.start()

    def __init__(self):
        self.isRunning = False
        self.motor = AdvancedMotor(pin=18, frequency=50, modifier=1)


def test_speed_control():
    try:
        controller = AdvancedMotorController()
        print("Starting motor...")
        controller.start_motor()

        # Speed up phase
        print("\nSpeeding up...")
        for _ in range(5):  # Speed up 5 times
            controller.speed_up()
            print(f"Current speed: {controller.motor.get_current_speed()}")
            sleep(2)  # Wait 2 seconds between each speed increase

        print("\nHolding max speed for 3 seconds...")
        sleep(3)

        # Slow down phase
        print("\nSlowing down...")
        for _ in range(5):  # Slow down 5 times
            controller.slow_down()
            print(f"Current speed: {controller.motor.get_current_speed()}")
            sleep(2)  # Wait 2 seconds between each speed decrease

        print("\nStopping motor...")
        controller.stop_motor()

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    finally:
        if hasattr(controller, 'motor'):
            controller.motor.cleanup()
        print("Cleanup completed")


if __name__ == "__main__":
    test_speed_control()