import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import threading
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
 
 
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler)
        ]
 
        settings = {
            'template_path': ''
        }
        tornado.web.Application.__init__(self, handlers, **settings)
 
class WebSocketInterface:
    def __init__(self):
        thread = threading.Thread(target=self.stream_thread)
        thread.start()
        ws_app = Application()
        server = tornado.httpserver.HTTPServer(ws_app)
        server.listen(8080)
        tornado.ioloop.IOLoop.instance().start()

    def stream_thread(self):
        stream = StreamInterface()

 
if __name__ == '__main__':
    interface = WebSocketInterface()