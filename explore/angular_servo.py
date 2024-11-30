from gpiozero import AngularServo
import time
from datetime import datetime


class ServoController:
    def __init__(self, pin=18, min_angle=0, max_angle=180,
                 min_pulse_width=0.5 / 1000, max_pulse_width=2.5 / 1000):
        """
        Initialize servo controller with configurable parameters
        """
        self.servo = AngularServo(pin,
                                  min_angle=min_angle,
                                  max_angle=max_angle,
                                  min_pulse_width=min_pulse_width,
                                  max_pulse_width=max_pulse_width)
        self.current_angle = 0
        print(f"[{self._get_timestamp()}] Servo initialized on pin {pin}")
        print(f"[{self._get_timestamp()}] Angle range: {min_angle}° to {max_angle}°")

    def _get_timestamp(self):
        """Get current timestamp for logging"""
        return datetime.now().strftime("%H:%M:%S.%f")[:-3]

    def set_angle(self, angle):
        """Set servo to specific angle"""
        print(f"[{self._get_timestamp()}] Setting angle to {angle}°")
        self.servo.angle = angle
        self.current_angle = angle

    def rotate_continuous(self, speed=1, direction=1):
        """
        Rotate servo continuously in one direction
        speed: value between 0 and 1 (1 being fastest)
        direction: 1 for clockwise, -1 for counter-clockwise
        """
        dir_text = "clockwise" if direction == 1 else "counter-clockwise"
        print(f"[{self._get_timestamp()}] Starting continuous rotation")
        print(f"[{self._get_timestamp()}] Direction: {dir_text}")
        print(f"[{self._get_timestamp()}] Speed: {speed * 100}%")

        step = speed * 2  # Adjust step size based on speed
        rotation_count = 0
        last_log_time = time.time()

        while True:
            try:
                current_time = time.time()
                # Update angle
                self.current_angle += step * direction
                print(f"Current angle {self.current_angle}")
                # Reset angle when reaching limits while maintaining direction
                # if direction == 1:  # Clockwise
                #     if self.current_angle >= 180:
                #         self.current_angle = 0
                #         rotation_count += 1
                #         print(f"[{self._get_timestamp()}] Completed {rotation_count} full rotation(s)")
                # # else:  # Counter-clockwise
                #     if self.current_angle <= 0:
                #     self.current_angle = 180
                #     rotation_count += 1
                #     print(f"[{self._get_timestamp()}] Completed {rotation_count} full rotation(s)")

                # Log current angle every 2 seconds
                if current_time - last_log_time >= 2:
                    print(f"[{self._get_timestamp()}] Current angle: {self.current_angle:.1f}°")
                    last_log_time = current_time

                self.servo.angle = self.current_angle
                time.sleep(0.02)  # Adjust delay for smooth motion

            except KeyboardInterrupt:
                print(f"\n[{self._get_timestamp()}] Stopping rotation")
                print(f"[{self._get_timestamp()}] Final angle: {self.current_angle:.1f}°")
                print(f"[{self._get_timestamp()}] Completed {rotation_count} full rotation(s)")
                break


# Example usage:
if __name__ == "__main__":
    servo = ServoController()
    # Continuous rotation in one direction at half speed
    # Use direction=1 for clockwise, direction=-1 for counter-clockwise
    servo.rotate_continuous(speed=0.2, direction=1)