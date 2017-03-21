#!/usr/bin/env python
from flask import Flask, render_template, Response
from time import sleep

# emulated camera
from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen(camera):

    """Video streaming generator function."""
    index = 0
    while True:
        frame = camera.get_frame(index)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        index += 1
        sleep(0.03)


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

class StreamInterface:
    def __init__(self):
        app.run(host='0.0.0.0', debug=False, threaded=True)

if __name__ == '__main__':
    stream = StreamInterface()