from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time
import cv2

server_ip = 'localhost'
sender = imagezmq.ImageSender(connect_to=f'tcp://{server_ip}:5555')
rpiName = '2'
'''
rpiName = socket.gethostname()
vs = VideoStream(usePiCamera=True).start()
# vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
    # read the frame from the camera and send it to the server
    frame = vs.read()
    sender.send_image(rpiName, frame)

vs = VideoStream(usePiCamera=True, resolution=(320, 240)).start()
'''
camera = cv2.VideoCapture(0)  # init the camera

while True:
    try:
        grabbed, frame = camera.read()  # grab the current frame
        frame = cv2.resize(frame, (640, 480))  # resize the frame
        sender.send_image(rpiName, frame)

    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        break