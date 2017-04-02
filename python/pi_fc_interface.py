from dronekit import connect, VehicleMode
import time

class PiDrone:
	#channel 1 -> roll, 2 -> pitch, 3 -> throttle, 4 -> yaw
	THROTTLE = '3'
	ROLL = '1'
	PITCH = '2'
	YAW = '4'
	
	ROLL_MID = 1492
	ROLL_RANGE = 372
	PITCH_MID = 1516
	PITCH_RANGE = 328
	YAW_MID = 1510
	YAW_RANGE = 366
	THROTTLE_MIN = 1161
	THROTTLE_RANGE = 660

	
	def test(self, value):
		print value
		print PiDrone.THROTTLE_MIN + int(PiDrone.THROTTLE_RANGE*value)
		return ''
	
	def fcConnect(self):
		print 'fcConnect'
		self.vehicle = connect('/dev/ttyACM0', wait_ready=True)
		return 'connected' if self.vehicle is not None else 'disconnected'		
	
	def fcInfo(self):
		print "Autopilot Firmware version: %s" % self.vehicle.version
		#print "Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp
		print "Global Location: %s" % self.vehicle.location.global_frame
		print "Global Location (relative altitude): %s" % self.vehicle.location.global_relative_frame
		print "Local Location: %s" % self.vehicle.location.local_frame    #NED
		print "Attitude: %s" % self.vehicle.attitude
		print "Velocity: %s" % self.vehicle.velocity
		print "GPS: %s" % self.vehicle.gps_0
		print "Groundspeed: %s" % self.vehicle.groundspeed
		print "Airspeed: %s" % self.vehicle.airspeed
		print "Gimbal status: %s" % self.vehicle.gimbal
		print "Battery: %s" % self.vehicle.battery
		print "EKF OK?: %s" % self.vehicle.ekf_ok
		print "Last Heartbeat: %s" % self.vehicle.last_heartbeat
		print "Rangefinder: %s" % self.vehicle.rangefinder
		print "Rangefinder distance: %s" % self.vehicle.rangefinder.distance
		print "Rangefinder voltage: %s" % self.vehicle.rangefinder.voltage
		print "Heading: %s" % self.vehicle.heading
		print "Is Armable?: %s" % self.vehicle.is_armable
		print "System status: %s" % self.vehicle.system_status.state
		print "Mode: %s" % self.vehicle.mode.name    # settable
		print "Armed: %s" % self.vehicle.armed    # settable

		print "\nPrint all parameters (iterate `vehicle.parameters`):"
		for key, value in self.vehicle.parameters.iteritems():
		    print " Key:%s Value:%s" % (key,value)

	def fcArm(self):
		#while vehicle.is_armable is False:
		#	print "Is Armable?: %s" % vehicle.is_armable
		self.vehicle.mode = VehicleMode('STABILIZE')
		self.vehicle.armed = True

		for x in xrange(100):
			if self.vehicle.armed:
				break
			print 'Trying to arm...\n'
			time.sleep(1)
		
		return 'armed' if self.vehicle.armed else 'disarmed'
	
	def fcDisarm(self):
		self.vehicle.armed = False
		for x in xrange(100):
			if ~self.vehicle.armed:
				break
			print 'Disarming...'
			time.sleep(1)
		
		return 'armed' if self.vehicle.armed else 'disarmed'

	def fcSetThrottle(self, value=0):
		self.vehicle.channels.overrides[PiDrone.THROTTLE] = PiDrone.THROTTLE_MIN + int(PiDrone.THROTTLE_RANGE*value)
		return '' if self.vehicle.armed else 'disarmed'

	def fcSetRoll(self, value=0):
		self.vehicle.channels.overrides[PiDrone.ROLL] = PiDrone.ROLL_MID + int(PiDrone.ROLL_RANGE*value)
		return '' if self.vehicle.armed else 'disarmed'

	def fcSetPitch(self, value=0):
		self.vehicle.channels.overrides[PiDrone.PITCH] = PiDrone.PITCH_MID + int(PiDrone.PITCH_RANGE*value)
		return '' if self.vehicle.armed else 'disarmed'

	def fcSetYaw(self, value=0):
		self.vehicle.channels.overrides[PiDrone.YAW] = PiDrone.YAW_MID + int(PiDrone.YAW_RANGE*value)
		return '' if self.vehicle.armed else 'disarmed'

	def fcDisconnect(self):
		self.fcSetThrottle()
		self.fcSetRoll()
		self.fcSetPitch()
		self.fcSetYaw()
		self.vehicle.channels.overrides = {}
		self.fcDisarm()
		self.vehicle.flush()

#vehicle.groundspeed = 3.2
#vehicle.airspeed = 3.2
#vehicle.simple_takeoff(10)

if __name__ == '__main__':
    drone = PiDrone()
    drone.fcConnect()
    drone.fcInfo()
    drone.fcArm()
    drone.fcSetThrottle(0.1)
    time.sleep(1)
    drone.fcSetThrottle()
    time.sleep(3)
    drone.fcSetThrottle(0.2)
    time.sleep(1)
    drone.fcSetThrottle()
    drone.fcDisconnect()
