
import math
import RPi.GPIO as GPIO


"""
http://www.toptechboy.com/raspberry-pi/raspberry-pi-lesson-28-controlling-a-servo-on-raspberry-pi-with-python/

pwm.start(dc)
pwm.ChangeDutyCyle(dc)
pwm.ChangeFrequency(fq)

dc = cycle de service
fq = frequence en hz (1hz = 1 cycle par seconde)
"""


class Servo():
	
	def __init__(self):
		
		self.sensibility = .3
		self.port = 24
		self.freq = 50

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.port, GPIO.OUT)

		self.pwm = GPIO.PWM(self.port, self.freq)	# broche 24, frequence de 50hz (50hz = 1/50 = 20 millisecondes)
		self.pwm.start(5)


	def update(self, last_x):
		"""
		last_x : -90 ~ 90
		xpos : 0 ~ 10 (5 = centre)
		"""

		xpos = ( last_x * self.sensibility ) + 6
		
		if xpos > 9.5:
			xpos = 9.5
		
		if xpos < 0.5:
			xpos = 0.5

#		print("lastx : " + str(last_x) + " - xpos : " + str(xpos) )

		self.pwm.ChangeDutyCycle(xpos)




	def stop(self):
		GPIO.cleanup()
