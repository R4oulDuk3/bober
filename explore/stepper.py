from gpiozero import OutputDevice
from time import sleep


class StepperMotor:
    def __init__(self, pin1, pin2, pin3, pin4):
        # Initialize the 4 control pins
        self.coil_A = OutputDevice(pin1)
        self.coil_B = OutputDevice(pin2)
        self.coil_C = OutputDevice(pin3)
        self.coil_D = OutputDevice(pin4)

        # Full step sequence (highest torque)
        self.step_sequence = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

    def step(self, steps, delay=0.002):
        """Rotate the motor by the specified number of steps"""
        for _ in range(abs(steps)):
            for pattern in (self.step_sequence if steps > 0 else reversed(self.step_sequence)):
                self.coil_A.value = pattern[0]
                self.coil_B.value = pattern[1]
                self.coil_C.value = pattern[2]
                self.coil_D.value = pattern[3]
                sleep(delay)

    def cleanup(self):
        """Turn off all coils and cleanup GPIO"""
        self.coil_A.off()
        self.coil_B.off()
        self.coil_C.off()
        self.coil_D.off()
        self.coil_A.close()
        self.coil_B.close()
        self.coil_C.close()
        self.coil_D.close()


def test_stepper():
    # Define the GPIO pins connected to ULN2003 driver
    # Modify these pins according to your wiring
    IN1, IN2, IN3, IN4 = 17, 18, 27, 22

    try:
        print("Initializing stepper motor...")
        motor = StepperMotor(IN1, IN2, IN3, IN4)

        print("Testing clockwise rotation...")
        motor.step(512)  # 512 steps = roughly one revolution
        sleep(1)

        print("Testing counter-clockwise rotation...")
        motor.step(-512)

        print("Testing small steps clockwise...")
        for _ in range(4):
            motor.step(128)  # Quarter turn
            sleep(0.5)

    except KeyboardInterrupt:
        print("\nTest stopped by user")

    finally:
        print("Cleaning up...")
        motor.cleanup()
        print("Test complete")


if __name__ == "__main__":
    test_stepper()