from interfaces.motor_interface import IMotorController
from gpiozero import PWMOutputDevice
from typing import Optional


class GradualMotor:
    def __init__(self, pin: int = 18, frequency: int = 1000):
        """Initialize the motor controller.

        Args:
            pin: GPIO pin number for PWM output
            frequency: PWM frequency in Hz
        """
        self.motor = PWMOutputDevice(pin, frequency=frequency, initial_value=0)
        self._current_speed = 0
        self._target_speed = 0
        self.step_size = 2  # Default step size for speed changes

    def set_speed(self, target_speed: int, step_size: Optional[int] = None) -> bool:
        """Execute a single step towards the target speed.

        Args:
            target_speed: Target speed percentage (0-100)
            step_size: Size of speed change step

        Returns:
            bool: True if target speed is reached, False if more steps needed
        """
        if not 0 <= target_speed <= 100:
            raise ValueError("Speed must be between 0 and 100")

        self._target_speed = target_speed
        step = step_size if step_size is not None else self.step_size

        # Determine direction and calculate next speed
        if self._current_speed < target_speed:
            next_speed = min(self._current_speed + step, target_speed)
        elif self._current_speed > target_speed:
            next_speed = max(self._current_speed - step, target_speed)
        else:
            return True  # Already at target speed

        # Apply the speed change
        self.motor.value = next_speed / 100.0
        self._current_speed = next_speed
        print(f"Current speed: {next_speed}%")

        # Return whether we've reached the target
        return next_speed == target_speed

    def get_current_speed(self) -> int:
        """Get the current motor speed percentage."""
        return self._current_speed

    def get_target_speed(self) -> int:
        """Get the target motor speed percentage."""
        return self._target_speed

    def stop(self) -> None:
        """Stop the motor."""
        self.motor.value = 0
        self._current_speed = 0
        self._target_speed = 0

    def cleanup(self) -> None:
        """Clean up GPIO resources."""
        self.stop()
        self.motor.off()
        self.motor.close()
        print("Motor cleanup completed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()

class SimpleMotorController(IMotorController):
    def is_running(self) -> bool:
        return self.is_running

    def get_speed(self) -> int:
        pass

    def slow_down(self) -> None:
        pass

    def speed_up(self) -> None:
        pass

    def __init__(self):
        """Initialize the motor controller with default values."""
        self.current_speed = 0.0
        self.is_running = False
        self.motor = GradualMotor()

    def start_motor(self) -> None:
        """Start the motor at the minimum speed."""
        if not self.is_running:
            self.is_running = True
            self.motor.set_speed(75, step_size=5)

    def stop_motor(self) -> None:
        """Gradually stop the motor."""
        if self.is_running:
            self.motor.stop()
            self.is_running = False

    def __del__(self):
        """Cleanup when object is destroyed."""
        self.stop_motor()
        if hasattr(self, 'motor'):
            self.motor.cleanup()