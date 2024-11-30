# 1. GPIOZero Example - Blinking LED and Button Input
from gpiozero import LED, Button
from signal import pause
import time


def gpiozero_example():
    # Create LED on GPIO17 and Button on GPIO2
    led = LED(17)
    button = Button(2)

    # Set up button to toggle LED
    button.when_pressed = led.on
    button.when_released = led.off

    # Alternative: Simple blinking pattern
    for _ in range(5):
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)

    # To keep the script running for the button
    pause()


# 2. LGPIO Example - PWM LED Control
import lgpio
from time import sleep


def lgpio_example():
    # Initialize LGPIO
    h = lgpio.gpiochip_open(0)

    # Configure GPIO18 as output for PWM
    gpio = 18
    lgpio.gpio_claim_output(h, gpio)

    # Create PWM with 1000Hz frequency
    freq = 1000
    lgpio.tx_pwm(h, gpio, freq, 0)  # Start with 0% duty cycle

    # Fade LED up and down
    try:
        for _ in range(2):
            # Fade up
            for duty in range(0, 100, 5):
                lgpio.tx_pwm(h, gpio, freq, duty)
                sleep(0.05)
            # Fade down
            for duty in range(100, -1, -5):
                lgpio.tx_pwm(h, gpio, freq, duty)
                sleep(0.05)
    finally:
        # Cleanup
        lgpio.gpio_free(h, gpio)
        lgpio.gpiochip_close(h)


# 3. PIGPIO Example - Servo Control
import pigpio
import time


def pigpio_example():
    # Initialize pigpio
    pi = pigpio.pi()
    if not pi.connected:
        return

    # Set up GPIO19 for servo control
    servo_pin = 19

    try:
        # Servo control (pulse width 500-2500 microseconds)
        # Center position
        pi.set_servo_pulsewidth(servo_pin, 1500)
        time.sleep(1)

        # Move to min position
        pi.set_servo_pulsewidth(servo_pin, 500)
        time.sleep(1)

        # Move to max position
        pi.set_servo_pulsewidth(servo_pin, 2500)
        time.sleep(1)

        # Return to center
        pi.set_servo_pulsewidth(servo_pin, 1500)
        time.sleep(1)

    finally:
        # Cleanup
        pi.set_servo_pulsewidth(servo_pin, 0)  # Turn off servo
        pi.stop()


if __name__ == "__main__":
    print("Running GPIOZero example...")
    gpiozero_example()

    print("\nRunning LGPIO example...")
    lgpio_example()

    print("\nRunning PIGPIO example...")
    pigpio_example()