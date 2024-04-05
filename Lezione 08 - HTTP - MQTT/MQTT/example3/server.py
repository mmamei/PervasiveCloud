import paho.mqtt.client as mqtt
import json

db = {}

def on_connect(client, userdata, flags, rc):
    #print('subscribe')
    mqtt_client.subscribe(default_topic)

def on_message(client, userdata, message):
    m = str(message.payload.decode("utf-8"))
    if message.topic in db:
        db[message.topic].append(json.loads(m))
    else:
        db[message.topic] = [json.loads(m)]

client_id = "server"
broker_ip = '34.154.23.168'#'broker.emqx.io'
broker_port = 1883
default_topic = "/sensors/#"
command_topic = '/cmd'

# Create a new MQTT Client
mqtt_client = mqtt.Client(client_id)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
print('connect',broker_ip, broker_port)
mqtt_client.connect(broker_ip, broker_port, keepalive=600)

mqtt_client.loop_start()

while(True):
    print('menu')
    print('1. stampa dati')
    print('2. blocca')
    print('3. riprendi')
    print('4. esci')
    c = input('inserisci comando')
    if c == '1':
        print(db)
    if c == '2':
        infot = mqtt_client.publish(command_topic, 'stop')
        infot.wait_for_publish()
    if c == '3':
        infot = mqtt_client.publish(command_topic, 'start')
        infot.wait_for_publish()
    if c == '4':
        break


mqtt_client.loop_stop()