from time import sleep

import RPi.GPIO as GPIO

duty_cycle = 14
servoPIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50)


p.start(duty_cycle) # value from 0 to 100



# p.ChangeDutyCycle(duty_cycle)
# # p.ChangeFrequency()
# p.ChangeDutyCycle(duty_cycle) # if want to update
# p.ChangeDutyCycle(duty_cycle)

sleep(4)

p.stop()
# import atexit
# atexit.register(GPIO.cleanup)