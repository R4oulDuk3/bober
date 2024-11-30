from gpiozero import DigitalInputDevice
import time

# Initialize the IR sensor
ir_sensor = DigitalInputDevice(17)

print("IR Sensor is running. Press CTRL+C to exit")

try:
    was_active = ir_sensor.value  # Store initial state

    while True:
        if ir_sensor.value != was_active:  # State has changed
            if ir_sensor.value:
                print("Object removed!")
            else:
                print("Object detected!")
            was_active = ir_sensor.value

        time.sleep(0.1)  # Small delay to prevent CPU overuse

except KeyboardInterrupt:
    print("\nExiting program")