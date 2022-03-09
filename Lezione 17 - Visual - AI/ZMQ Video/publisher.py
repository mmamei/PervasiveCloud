import time

import cv2
import msgpack
import zmq
import base64
from video_config import *
import json

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect(f'tcp://{broker_ip}:{broker_port_pub}')

camera = cv2.VideoCapture(0)  # init the camera

while True:
    try:
        now = time.time()
        grabbed, frame = camera.read()  # grab the current frame
        frame = cv2.resize(frame, (640, 480))  # resize the frame
        encoded, buffer = cv2.imencode('.jpg', frame)
        img_as_text = base64.b64encode(buffer).decode('utf-8')
        #message = img_as_text
        message = json.dumps({'time': now, 'image': img_as_text})
        footage_socket.send_string(f'{default_topic}-{message}')


    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        break