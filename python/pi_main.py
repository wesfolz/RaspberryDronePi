import threading

from pi_webSocketServer import WebSocketInterface
from pi_stream import StreamInterface
from pi_fc_interface import PiDrone

class Main:
	def __init__(self):
		websocketThread = threading.Thread(target=self.websocket_thread)
		websocketThread.start()
		streamThread = threading.Thread(target=self.stream_thread)
		streamThread.start()
		self.drone = PiDrone()

	def stream_thread(self):
		stream = StreamInterface()

	def websocket_thread(self):
		websocket = WebSocketInterface(self.translate_command)

	def translate_command(self, callerRef, command):
		print 'translate command ' + command
		try:
			#command should be in the form of 'method,argument'
			tokens = command.split[',']
			print tokens
			#get 'method' attr frome drone, pass in 'argument'
			getattr(self.drone, tokens[0])(int(tokens[1]))
		except (KeyError, IndexError, AttributeError):
			return False

		return True

if __name__ == '__main__':
	Main()