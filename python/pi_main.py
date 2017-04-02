import threading

from pi_webSocketServer import WebSocketInterface
from pi_stream import StreamInterface
from pi_fc_interface import PiDrone

class Main:
	def __init__(self):
		websocketThread = threading.Thread(target=self.websocketThread)
		websocketThread.start()
		self.streamThread = threading.Thread(target=self.streamThread)
		#self.streamThread.start()
		self.drone = PiDrone()

	def startStream(self):
		self.streamThread.start()
		return 'streaming'

	def streamThread(self):
		self.stream = StreamInterface()

	def websocketThread(self):
		websocket = WebSocketInterface(self.translateCommand)

	def translateCommand(self, callerRef, command):
		print 'translate command ' + command
		try:
			#command should be in the form of 'method,argument'
			tokens = command.split(',')
			print tokens
			attrOwner = self.drone
			if hasattr(self, tokens[0]):
				attrOwner = self
			#get 'method' attr frome drone, pass in 'argument'
			if len(tokens) == 1:
				result = getattr(attrOwner, tokens[0])()
			else:
				result = getattr(attrOwner, tokens[0])(float(tokens[1]))
		except (KeyError, IndexError, AttributeError):
			print 'exception'
			return 'Failed'

		print 'found method ' + result
		return result

if __name__ == '__main__':
	Main()
