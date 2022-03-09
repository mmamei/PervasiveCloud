import time

import cv2
#import msgpack
import zmq
import base64
from video_config import *
import json

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect(f'tcp://{broker_ip}:{broker_port_pub}')

camera = cv2.VideoCapture(0)  # init the camera
#camera.set(cv2.CAP_PROP_FPS, int(1))

width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(width, height)

start_time = time.time()
x = 1 # displays the frame rate every 1 second
counter = 0

while True:
    try:
        now = time.time()
        grabbed, frame = camera.read()  # grab the current frame

        counter += 1
        if (time.time() - start_time) > x:
            print("FPS: ", counter / (time.time() - start_time))
            counter = 0
            start_time = time.time()

        #frame = cv2.resize(frame, (320, 256))  # resize the frame
        #print('Resized Dimensions : ', frame.shape)

        image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        footage_socket.send_multipart([bytearray(default_topic.encode()), str(now).encode(), image_bytes])
        time.sleep(0.05)


    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        break