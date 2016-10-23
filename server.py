#!/usr/bin/python

import math
import time
from threading import Thread, RLock
import tornado.ioloop
import tornado.web

from servo import Servo
from gyro import Gyro
from led import Led
from gps import Gps




class WebServer(tornado.web.RequestHandler):
    def get(self):

		# brut
		#self.write(str(gyro.rotation_x)+" "+str(gyro.rotation_y)+" "+str(gyro.rotation_z)+" "+str(gyro.gyro_scaled_x))

		# pondere
		self.write(str(gyro.last_x)+" "+str(gyro.last_y)+" "+str(gyro.last_z)+" "+str(gyro.gyro_scaled_x))




class Tache(Thread):

    def __init__(self, task):
        Thread.__init__(self)
        self.daemon = True
        self.task = task

    def run(self):
        if(self.task == "gyro"):
                self.gyro()

        if(self.task == "servo"):
                 self.servo()

        if(self.task == "webserver"):
                self.webserver()

        if(self.task == "led"):
                self.led()

        if(self.task == "gps"):
                self.gps()

    def gyro(self):
		while True:
			gyro.update()
			time.sleep(0.1)

    def servo(self):
        while True:
            servo.update(gyro.last_x)
            time.sleep(0.1)

    def webserver(self):
        app = tornado.web.Application([
            (r"/", WebServer)
        ])
        app.listen(8080)
        tornado.ioloop.IOLoop.current().start()

    def led(self):
    	led.start()

    def gps(self):
		while True:
			gps.update()
			time.sleep(0.1)
        



if __name__ == "__main__":

	gyro = Gyro()
	servo = Servo()
	led = Led()
	gps = Gps()

	tgy = Tache("gyro")
	tse = Tache("servo")
	tws = Tache("webserver")
	tle = Tache("led")
	tgp = Tache("gps")

	tgy.start()
	tse.start()
	tws.start()
	tle.start()
	tgp.start()

	try:
		while True:
			time.sleep(100)

	except KeyboardInterrupt:
		print("fin")
		servo.stop()
		quit()



