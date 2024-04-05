# For this example we rely on the Paho MQTT Library for Python
# You can install it through the following command: pip install paho-mqtt
import time

import paho.mqtt.client as mqtt
import cv2 as cv
import numpy as np
import base64
import json
from video_config import *

latencies_pre = []
latencies_post = []
img = np.zeros((240, 320, 3), np.uint8)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt_client.subscribe(default_topic)
    print("Subscribed to: " + default_topic)

def on_message(client, userdata, message):
    print(message, userdata)
    global img
    pre_des = time.time()
    dict = json.loads(message.payload)
    print('DT deserializzazione',(time.time()-pre_des)*1000)
    print('PAYLOAD ',len(message.payload))
    latencies_pre.append((time.time() - dict['time']) * 1000)
    # Decoding the message
    x = base64.b64decode(dict['image'].encode('utf-8'))
    # converting into numpy array from buffer
    npimg = np.frombuffer(x, dtype=np.uint8)
    # Decode to Original Frame
    img = cv.imdecode(npimg, 1)
    latencies_post.append((time.time() - dict['time']) * 1000)


# Configuration variables
client_id = "clientId0001-Consumer"

# Create a new MQTT Client
# mqtt_client = Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)
mqtt_client = mqtt.Client(client_id)
# Attack Paho OnMessage Callback Method
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect

# Connect to the target MQTT Broker
#mqtt_client.username_pw_set(username=user, password=passw)
mqtt_client.connect(broker_ip, broker_port)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqtt_client.loop_start()

while True:
    cv.imshow("Consumer", img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the Thread
mqtt_client.loop_stop()

print('PRE')
print('Mean =',np.mean(latencies_pre))
print('Median =',np.median(latencies_pre))
print('SD =' ,np.std(latencies_pre))
print('POST')
print('Mean =',np.mean(latencies_post))
print('Median =',np.median(latencies_post))
print('SD =' ,np.std(latencies_post))