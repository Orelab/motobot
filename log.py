
from datetime import datetime


class Log():
	
	def __init__(self):
		self.log = "/home/pi/motobot/" + datetime.now().isoformat() + ".txt"

		line = "datetime;latitude;longitude;altitude;" \
			+ "rotation_x;rotation_y;rotation_z;" \
			+ "pondere_x;pondere_y;pondere_z;" \
			+ "accel_x;accel_y;accel_z\r\n"

		with open(self.log, "a") as logfile:
			logfile.write(line)


	def write(self, gps, gyro):
		"""
			time
			latitude
			longitude
			altitude
			rotation x
			rotation y
			rotation z
			rotation pondere x
			rotation pondere y
			rotation pondere z
			acceleration x
			acceleration y
			acceleration z
			direction	(soon)
			
			( for gyro : last_x=pondere ; rotation_x=brut )
		"""
				
		line = datetime.now().isoformat() + ";" \
			+ str(gps.latitude) + ";" \
			+ str(gps.longitude) + ";" \
			+ str(gps.altitude) + ";" \
			+ str(gyro.rotation_x) + ";" \
			+ str(gyro.rotation_y) + ";" \
			+ str(gyro.rotation_z) + ";" \
			+ str(gyro.last_x) + ";" \
			+ str(gyro.last_y) + ";" \
			+ str(gyro.last_z) + ";" \
			+ str(gyro.accel_scaled_x) + ";" \
			+ str(gyro.accel_scaled_y) + ";" \
			+ str(gyro.accel_scaled_z) + "\r\n"

		with open(self.log, "a") as logfile:
			logfile.write(line)
		
		#print line


