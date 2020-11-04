from flask import render_template, Response

from . import parking
from .camera import VideoCamera


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        )


@parking.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@parking.route('/video', methods=['GET'])
def video_feed():
    return Response(
        gen(VideoCamera()),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )
