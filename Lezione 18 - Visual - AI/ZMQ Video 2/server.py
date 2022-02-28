# import the necessary packages
from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq
import argparse
import imutils
import cv2

# initialize the ImageHub object
imageHub = imagezmq.ImageHub()
frameDict = {}
lastActive = {}
lastActiveCheck = datetime.now()

while True:
	# receive RPi name and frame from the RPi and acknowledge
	# the receipt
	(rpiName, frame) = imageHub.recv_image()
	imageHub.send_reply(b'OK')
	# if a device is not in the last active dictionary then it means
	# that its a newly connected device
	if rpiName not in lastActive.keys():
		print("[INFO] receiving data from {}...".format(rpiName))
	# record the last active time for the device from which we just
	# received a frame
	lastActive[rpiName] = datetime.now()
	cv2.putText(frame, rpiName, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	frameDict[rpiName] = frame

	for k,v in frameDict.items():
		cv2.imshow(k, v)
	cv2.waitKey(1)
cv2.destroyAllWindows()