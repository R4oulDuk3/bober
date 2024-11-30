import RPi.GPIO as GPIO

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
    # To set voltage to about 1.65V (50% of 3.3V)
    pwm.ChangeDutyCycle(50)

    # Your main code here

except KeyboardInterrupt:
    # Clean up
    pwm.stop()
    GPIO.cleanup()