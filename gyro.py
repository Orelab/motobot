#!/usr/bin/python

import smbus
import math


class Gyro():
	
	def __init__(self):

		# Power management registers
		self.power_mgmt_1 = 0x6b
		self.power_mgmt_2 = 0x6c

		# gyro
		self.gyro_scale = 131.0
		self.accel_scale = 16384.0

		self.K = 0.7
		self.K1 = 1 - self.K
		self.time_diff = 0.005

		self.bus = smbus.SMBus(1)
		self.address = 0x68

		# Now wake the 6050 up as it starts in sleep mode
		self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)

		self.read_all()
		
		self.last_x = self.get_x_rotation(self.accel_scaled_x, self.accel_scaled_y, self.accel_scaled_z)
		self.last_y = self.get_y_rotation(self.accel_scaled_x, self.accel_scaled_y, self.accel_scaled_z)
		self.last_z = self.get_z_rotation(self.accel_scaled_x, self.accel_scaled_y, self.accel_scaled_z)
		
		self.gyro_offset_x = self.gyro_scaled_x 
		self.gyro_offset_y = self.gyro_scaled_y
		self.gyro_offset_z = self.gyro_scaled_z
		
		self.gyro_total_x = self.last_x - self.gyro_offset_x
		self.gyro_total_y = self.last_y - self.gyro_offset_y
		self.gyro_total_z = self.last_z - self.gyro_offset_z


	def update(self):

		self.read_all()
		
		self.gyro_scaled_x -= self.gyro_offset_x
		self.gyro_scaled_y -= self.gyro_offset_y
		self.gyro_scaled_z -= self.gyro_offset_z
		
		self.gyro_x_delta = self.gyro_scaled_x * self.time_diff
		self.gyro_y_delta = self.gyro_scaled_y * self.time_diff
		self.gyro_z_delta = self.gyro_scaled_z * self.time_diff
		
		self.gyro_total_x += self.gyro_x_delta
		self.gyro_total_y += self.gyro_y_delta
		self.gyro_total_z += self.gyro_z_delta
		
		self.rotation_x = self.get_x_rotation(self.accel_scaled_x, self.accel_scaled_y, self.accel_scaled_z)
		self.rotation_y = self.get_y_rotation(self.accel_scaled_x, self.accel_scaled_y, self.accel_scaled_z)
		self.rotation_z = self.get_z_rotation(self.accel_scaled_x, self.accel_scaled_y, self.accel_scaled_z)
		
		self.last_x = self.K * (self.last_x + self.gyro_x_delta) + (self.K1 * self.rotation_x)
		self.last_y = self.K * (self.last_y + self.gyro_y_delta) + (self.K1 * self.rotation_y)
		self.last_z = self.K * (self.last_z + self.gyro_z_delta) + (self.K1 * self.rotation_z)
	
	
	def read_all(self):
		raw_gyro_data = self.bus.read_i2c_block_data(self.address, 0x43, 6)
		raw_accel_data = self.bus.read_i2c_block_data(self.address, 0x3b, 6)
		
		self.gyro_scaled_x = self.twos_compliment((raw_gyro_data[0] << 8) + raw_gyro_data[1]) / self.gyro_scale
		self.gyro_scaled_y = self.twos_compliment((raw_gyro_data[2] << 8) + raw_gyro_data[3]) / self.gyro_scale
		self.gyro_scaled_z = self.twos_compliment((raw_gyro_data[4] << 8) + raw_gyro_data[5]) / self.gyro_scale
		
		self.accel_scaled_x = self.twos_compliment((raw_accel_data[0] << 8) + raw_accel_data[1]) / self.accel_scale
		self.accel_scaled_y = self.twos_compliment((raw_accel_data[2] << 8) + raw_accel_data[3]) / self.accel_scale
		self.accel_scaled_z = self.twos_compliment((raw_accel_data[4] << 8) + raw_accel_data[5]) / self.accel_scale

	def twos_compliment(self, val):
		if (val >= 0x8000):
			return -((65535 - val) + 1)
		else:
			return val

	
	def dist(self, a, b):
		return math.sqrt((a * a) + (b * b))
	
	def get_y_rotation(self, x,y,z):
		radians = math.atan2(x, self.dist(y,z))
		return -math.degrees(radians)
	
	def get_x_rotation(self, x,y,z):
		radians = math.atan2(y, self.dist(x,z))
		return math.degrees(radians)
	
	def get_z_rotation(self, x,y,z):
		radians = math.atan2(z, self.dist(y,x))
		return math.degrees(radians)







