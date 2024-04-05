# For this example we rely on the Paho MQTT Library for Python
# You can install it through the following command: pip install paho-mqtt

import paho.mqtt.client as mqtt
import time
import cv2 as cv
import base64
import json
import numpy as np
from video_config import *
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


# Configuration variables
client_id = "clientId0001-Producer"


mqtt_client = mqtt.Client(client_id)
mqtt_client.on_connect = on_connect

print("Connecting to "+ broker_ip + " port: " + str(broker_port))
#mqtt_client.tls_set()
#mqtt_client.username_pw_set(username=user, password=passw)
mqtt_client.connect(broker_ip, broker_port)


mqtt_client.loop_start()
mqtt_client.max_inflight_messages_set(10)
mqtt_client.max_queued_messages_set(10)
# MQTT Paho Publish method with all the available parameters
# mqtt_client.publish(topic, payload=None, qos=0, retain=False)

vid = cv.VideoCapture(0)
message_id = 0
while True:
    # Read Frame
    now = time.time()
    _, frame = vid.read()
    #frame = cv.resize(frame, (640, 480))  # resize the frame
    cv.imshow('frame', frame)
    # Encoding the Frame
    #_, buffer = cv.imencode('.png', frame)
    # Converting into encoded bytes
    #img_as_text = base64.b64encode(buffer)
    #message = json.dumps({'time':now,'image': img_as_text.decode('utf-8')})
    # Publishig the Frame on the Topic home/server
    print((time.time() - now) * 1000)
    #mqtt_client.publish(default_topic, message,qos=0)

    #time.sleep(0.5)


# After the loop release the cap object
vid.release()
mqtt_client.loop_stop()