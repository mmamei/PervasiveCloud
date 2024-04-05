# For this example we rely on the Paho MQTT Library for Python
# You can install it through the following command: pip install paho-mqtt
import time

import paho.mqtt.client as mqtt


# Full MQTT client creation with all the parameters. The only one mandatory in the ClientId that should be unique
# mqtt_client = Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt_client.subscribe(default_topic)
    print("Subscribed to: " + default_topic)

def on_disconnect(client, userdata, rc):
    print("disConnected with result code ")


# Define a callback method to receive asynchronous messages
def on_message(client, userdata, message):
    print(message,userdata)
    print("\n##########################################################")
    print("message received: ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)
    print("##########################################################")


# Configuration variables
client_id = "clientId0002-Consumer"
#broker_ip = "127.0.0.1"
#broker_ip = "35.195.87.164"
#broker_port = 1883

#broker_ip = 'broker.mqttdashboard.com'
#broker_port = 1883

broker_ip = 'broker.emqx.io'
broker_port = 1883

default_topic = "/stm/#"

# Create a new MQTT Client
mqtt_client = mqtt.Client(client_id)

# Attack Paho OnMessage Callback Method
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
# Connect to the target MQTT Broker
print('connect',broker_ip, broker_port)
#mqtt_client.username_pw_set(username="pcloud23", password="pcloud23")
mqtt_client.connect(broker_ip, broker_port, keepalive=600)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

mqtt_client.loop_start()

print('ciao')
input('inserisci qualcosa per terminare')

mqtt_client.loop_stop()