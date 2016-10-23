#!/usr/bin/python

import math
import RPi.GPIO as GPIO


"""

pwm.start(dc)
pwm.ChangeDutyCyle(dc)
pwm.ChangeFrequency(fq)

dc = cycle de service
fq = frequence en hz (1hz = 1 cycle par seconde)
"""


class Servo():
	
	def __init__(self):

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(24, GPIO.OUT)

		self.pwm = GPIO.PWM(24, 100)	# broche, frequence
		self.pwm.start(5)
#		self.pwm.ChangeFrequency(10000)


	def update(self, last_x):
		xpos = ( last_x + 90 ) / 10 + 2.5
#		xpos = last_x

		print("lastx : " + str(math.fabs(last_x)) + " - xpos : " + str(math.fabs(xpos)) )
		self.pwm.ChangeDutyCycle(math.fabs(xpos))


	def stop(self):
		GPIO.cleanup()