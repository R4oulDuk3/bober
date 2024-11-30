from time import sleep

from gpiozero import DistanceSensor

sensor = DistanceSensor(17, 27)

while True:
    print(f"Distance to nearest object: {sensor.distance * 100}cm")
    sleep(0.1)

# below 5 box is present, otherwise