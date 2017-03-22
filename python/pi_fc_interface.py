from dronekit import connect, VehicleMode
import time

class PiDrone:
	#channel 1 -> roll, 2 -> pitch, 3 -> throttle, 4 -> yaw
	THROTTLE = '3'
	ROLL = '1'
	PITCH = '2'
	YAW = '4'
	
	def test(self):
		print 'value' 
	
	def fcConnect(self):
		self.vehicle = connect('/dev/ttyACM0', wait_ready=True)
	
	def fcInfo(self):
		print "Autopilot Firmware version: %s" % vehicle.version
		#print "Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp
		print "Global Location: %s" % vehicle.location.global_frame
		print "Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
		print "Local Location: %s" % vehicle.location.local_frame    #NED
		print "Attitude: %s" % vehicle.attitude
		print "Velocity: %s" % vehicle.velocity
		print "GPS: %s" % vehicle.gps_0
		print "Groundspeed: %s" % vehicle.groundspeed
		print "Airspeed: %s" % vehicle.airspeed
		print "Gimbal status: %s" % vehicle.gimbal
		print "Battery: %s" % vehicle.battery
		print "EKF OK?: %s" % vehicle.ekf_ok
		print "Last Heartbeat: %s" % vehicle.last_heartbeat
		print "Rangefinder: %s" % vehicle.rangefinder
		print "Rangefinder distance: %s" % vehicle.rangefinder.distance
		print "Rangefinder voltage: %s" % vehicle.rangefinder.voltage
		print "Heading: %s" % vehicle.heading
		print "Is Armable?: %s" % vehicle.is_armable
		print "System status: %s" % vehicle.system_status.state
		print "Mode: %s" % vehicle.mode.name    # settable
		print "Armed: %s" % vehicle.armed    # settable

		print "\nPrint all parameters (iterate `vehicle.parameters`):"
		for key, value in vehicle.parameters.iteritems():
		    print " Key:%s Value:%s" % (key,value)

	def fcArm(self):
		#while vehicle.is_armable is False:
		#	print "Is Armable?: %s" % vehicle.is_armable
		self.vehicle.mode = VehicleMode('STABILIZE')
		self.vehicle.armed = True

		while not self.vehicle.armed:
			print 'Trying to arm...\n'
			time.sleep(1)

	def fcDisarm(self):
		self.vehicle.armed = False

	def fcSetThrottle(self, value=1000):
		self.vehicle.channels.overrides[PiDrone.THROTTLE] = value

	def fcSetRoll(self, value=0):
		self.vehicle.channels.overrides[PiDrone.ROLL] = value

	def fcSetPitch(self, value=0):
		self.vehicle.channels.overrides[PiDrone.PITCH] = value

	def fcSetYaw(self, value=0):
		self.vehicle.channels.overrides[PiDrone.YAW] = value

	def fcDisconnect(self):
		self.apmSetThrottle()
		self.apmSetRoll()
		self.apmSetPitch()
		self.apmSetYaw()
		self.vehicle.channels.overrides = {}
		self.apmDisarm()
		self.vehicle.flush()

#vehicle.groundspeed = 3.2
#vehicle.airspeed = 3.2
#vehicle.simple_takeoff(10)

if __name__ == '__main__':
    drone = PiDrone()
    drone.fcConnect()
    drone.fcInfo()
    drone.fcArm()
    drone.fcSetThrottle(1200)
    time.sleep(1)
    drone.fcSetThrottle(1500)
    time.sleep(1)
    drone.fcSetThrottle(1000)
    drone.fcDisconnect()
