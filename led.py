#!/usr/bin/python


"""
make a led blinking, and learn how to use GPIO Pulse Width Modulation (PWM)

https://mespotesgeek.fr/fr/variation-de-puissance-electrique-via-raspberry/
https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/

"""



import RPi.GPIO as GPIO 
import time

pin = 4

class Led():

	def __init__(self):

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.OUT)

	"""		
	def start(self):
		LED = GPIO.PWM(pin, 1)	# canal 4, frequence 1 seconde (0.5 = 2s)
		LED.start(2)	# cycle 50%
		
		while True:
			time.sleep(1)
	"""

	def blink(self):
		LED = GPIO.PWM(pin, 1)	# canal 4, frequence 1 seconde (0.5 = 2s)
		LED.start(2)	# cycle 50%
		time.sleep(.5)



