import paho.mqtt.client as mqtt
import time
import json

client_id = "sensor1"
broker_ip = '34.154.23.168'#'broker.emqx.io'
broker_port = 1883
default_topic = "/sensors/1"
command_topic = '/cmd'


send = True

def on_connect(client, userdata, flags, rc):
    #print('subscribe')
    mqtt_client.subscribe(command_topic)

def on_message(client, userdata, message):
    m = str(message.payload.decode("utf-8"))
    global send
    if m == 'stop':
        send = False
    if m == 'start':
        send = True

mqtt_client = mqtt.Client(client_id)
print(f'Connecting to {broker_ip} port: {broker_port}')
mqtt_client.connect(broker_ip, broker_port)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


mqtt_client.loop_start()
with open('CleanData_PM10.csv') as f:
    for l in f.readlines()[1:]:
        data,val = l.strip().split(',')
        if send:
            print(data,val)
            payload_string = json.dumps({'data':data,'val':float(val)})
            infot = mqtt_client.publish(default_topic, payload_string)
            infot.wait_for_publish()
            print(f"Message Sent: Topic: {default_topic} Payload: {payload_string}")
        time.sleep(5)

mqtt_client.loop_stop()