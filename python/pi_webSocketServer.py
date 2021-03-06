import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
from pi_stream import StreamInterface

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    @staticmethod
    def callback(arg1, arg2):
        return ''

    def open(self):
        print("Socket opened.")
	self.write_message('socketOpened')
 
    def on_message(self, message):
        #self.write_message("Your message was: " + message)
        print("Received message: " + message)
	reply = str(WebSocketHandler.callback(self, message))
	if reply:
		print 'reply ' + reply 
        	self.write_message(reply)

    def on_close(self):
        print("Socket closed.")
 
class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
 
class WebSocketInterface:
    def __init__(self, messageCallback):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler)
        ]
        WebSocketHandler.callback = messageCallback
        ws_app = tornado.web.Application(handlers)
        server = tornado.httpserver.HTTPServer(ws_app)
        server.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
 
if __name__ == '__main__':
    interface = WebSocketInterface()
