import os
import random
import time
import queue
import threading

from flask import render_template, Response, current_app, jsonify
from PIL import Image
import cv2

from . import parking
from .camera import VideoCamera
from .inference import make_inference
from .threading import ThreadedInference


parking_state = {
    'empty_spaces': [1, 2, 3, 4],
    'parked_spaces': [5, 6, 7, 8],
}
qu = queue.Queue(maxsize=5)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        )


def genim(camera, imagemap, displaygrid):
    global parking_state

    qu.put(parking_state)

    while True:
        frame = cv2.imread(os.path.join('data', 'parking_lot.png'))
        parked, empty = [], []
        image_table = {}

        for slot in imagemap.keys():
            x1, y1 = imagemap[slot]['top']
            x2, y2 = imagemap[slot]['bottom']
            roi = frame[y1:y2, x1:x2]

            image_table[slot] = Image.fromarray(roi)

        try:
            parking_state = qu.get(0)

            ThreadedInference(qu, image_table).start()
        except queue.Empty:
            pass
        finally:
            for slot in parking_state['empty_spaces']:
                x1, y1 = imagemap[str(slot)]['top']
                x2, y2 = imagemap[str(slot)]['bottom']

                frame = cv2.rectangle(
                    frame, (x1, y1), (x2, y2), (0, 255, 0), thickness=4
                )
            for slot in parking_state['parked_spaces']:
                x1, y1 = imagemap[str(slot)]['top']
                x2, y2 = imagemap[str(slot)]['bottom']

                frame = cv2.rectangle(
                    frame, (x1, y1), (x2, y2), (0, 0, 255), thickness=4
                )

        ret, frame = cv2.imencode('.jpg', frame)
        frame = frame.tobytes()
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n\r\n'
        )


@parking.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@parking.route('/video', methods=['GET'])
def video_feed():
    imagemap = current_app.config['IMAGE_MAP']['slots']
    displaygrid = current_app.config['IMAGE_MAP']['display_grid']

    return Response(
        genim(VideoCamera(), imagemap, displaygrid),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@parking.route('/spaces', methods=['GET'])
def parking_spaces():
    return jsonify(
        parking_state
    )
