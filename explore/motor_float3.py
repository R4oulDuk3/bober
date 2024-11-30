import lgpio
import time

# Initialize LGPIO
h = lgpio.gpiochip_open(0)
pin = 18

# Configure PWM on GPIO 18 (frequency in Hz, duty cycle 0-100%)
frequency = 1000  # 1kHz frequency
lgpio.tx_pwm(h, pin, frequency, 90)  # 90% duty cycle (equivalent to 0.9)

print("Running")
time.sleep(5)
print("Stopping")

# Stop PWM
lgpio.tx_pwm(h, pin, frequency, 0)

# Cleanup
lgpio.gpiochip_close(h)