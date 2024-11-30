from time import sleep

from gpiozero import DistanceSensor

sensor = DistanceSensor(17, 27)

while True:
    print(f"Distance to nearest object: {sensor.distance}m")
    sleep(0.5)

