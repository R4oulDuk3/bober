import RPi.GPIO as GPIO
import time  # Import time module for sleep

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Choose a GPIO pin (e.g., GPIO18, which is physical pin 12)
output_pin = 18

# Set up the pin as output
GPIO.setup(output_pin, GPIO.OUT)

# Create PWM instance at 1000Hz
pwm = GPIO.PWM(output_pin, 1000)

# Start PWM with 0% duty cycle
pwm.start(0)

try:

    # Optional: Create a simple speed pattern
    print("Changing speeds...")
    speeds = [10, 50, 75]
    for speed in speeds:
        print(f"Changing to {speed}% speed")
        pwm.ChangeDutyCycle(speed)
        time.sleep(4)  # Run at each speed for 2 seconds

    print("Stopping motor...")
    pwm.ChangeDutyCycle(0)
    time.sleep(1)  # Brief pause before cleanup

except KeyboardInterrupt:
    print("\nProgram stopped by user")

finally:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleanup completed")