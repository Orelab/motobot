
import serial
import os


"""

http://raspberry-pi.developpez.com/cours-tutoriels/projets-rpi-zero/traceur-gps/#LV
http://aprs.gids.nl/nmea/

"""


class Gps():
	
	def __init__(self):
		self.firstFixFlag = False
		self.firstFixDate = ""

		self.latitude = ""
		self.longitude = ""
		self.altitude = ""

		self.ser = serial.Serial(
		    port='/dev/ttyACM0',\
		    baudrate=9600,\
		    parity=serial.PARITY_NONE,\
		    stopbits=serial.STOPBITS_ONE,\
		    bytesize=serial.EIGHTBITS,\
    		timeout=1
		)



	def degrees_to_decimal(self, data, hemisphere):
	    try:
	        decimalPointPosition = data.index('.')
	        degrees = float(data[:decimalPointPosition-2])
	        minutes = float(data[decimalPointPosition-2:])/60
	        output = degrees + minutes
	
	        if hemisphere is 'N' or hemisphere is 'E':
	            return output
	
	        if hemisphere is 'S' or hemisphere is 'W':
	            return -output
	
	    except:
	        return ""



	def parse_GPRMC(self, data):
	    data = data.split(',')
	    dict = {
	        'fix_time': data[1],
	        'validity': data[2],
	        'latitude': data[3],
	        'latitude_hemisphere' : data[4],
	        'longitude' : data[5],
	        'longitude_hemisphere' : data[6],
	        'speed': data[7],
	        'true_course': data[8],
	        'fix_date': data[9],
	        'variation': data[10],
	        'variation_e_w' : data[11],
	        'checksum' : data[12],
	        'decimal_latitude' : self.degrees_to_decimal(data[3], data[4]),
	        'decimal_longitude' : self.degrees_to_decimal(data[5], data[6])
	    }
	    return dict



	def parse_GPGGA(self, data):
	    data = data.split(',')
	    dict = {
	        'fix_time': data[1],
	        'latitude': data[2],
	        'latitude_hemisphere': data[3],
	        'longitude': data[4],
	        'longitude_hemisphere': data[5],
	        'quality' : data[6],
	        'satellites' : data[7],
	        'hdop' : data[8],
	        'altitude': data[9],
	        'wgs84': data[10],
	        'dgps_time': data[11],
	        'dgps_id': data[12],
	        'checksum' : data[13],
	        'checksum' : data[14],
	        'decimal_latitude' : self.degrees_to_decimal(data[2], data[3]),
	        'decimal_longitude' : self.degrees_to_decimal(data[4], data[5])
	    }
	    return dict



	def update(self):
		line = self.ser.readline()
		#print line
		
		"""
		Fetching latitude/longitude
		"" "
		if "$GPRMC" in line:
			gpsData = self.parse_GPRMC(line)
			
			if gpsData['validity'] == "A":
				if self.firstFixFlag is False:
					self.firstFixDate = gpsData['fix_date'] + "-" + gpsData['fix_time']
					self.firstFixFlag = True
				
				else:
					self.latitude = str(gpsData['decimal_latitude'])
					self.longitude = str(gpsData['decimal_longitude'])
					#print "lat=" + self.latitude + " lng=" + self.latitude
			
			else:
				self.latitude = ""
				self.longitude = ""
				#print "GPS desynchronized"
		"""


		"""
		Fetching latitude/longitude/altitude
		"""
		if "$GPGGA" in line:
			gpsData = self.parse_GPGGA(line)

			if gpsData["quality"] != 0:
				self.latitude = str(gpsData['decimal_latitude'])
				self.longitude = str(gpsData['decimal_longitude'])
				self.altitude = str(gpsData['altitude'])
			"""
				print "lat=" + self.latitude \
				   + " lng=" + self.longitude \
				   + " alt=" + self.altitude

			else:
				print "GPS desynchronized"
			"""


	def stop(self):
		GPIO.cleanup()


