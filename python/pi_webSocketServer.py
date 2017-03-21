import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
from pi_stream import StreamInterface

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Socket opened.")
 
    def on_message(self, message):
        self.write_message(u"Your message was: " + message)
        print("Received message: " + message)
 
    def on_close(self):
        print("Socket closed.")
 
class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
 
class WebSocketInterface:
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler)
        ]
        ws_app = tornado.web.Application(handlers)
        server = tornado.httpserver.HTTPServer(ws_app)
        server.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
 
if __name__ == '__main__':
    interface = WebSocketInterface()