import paho.mqtt.client as mqtt
from flask import Flask,request
import json

data = {}

def on_connect(client, userdata, flags, rc):
    mqtt_client.subscribe(default_topic)
def on_message(client, userdata, message):
    #print("message topic: ", message.topic)
    #print("message received: ", str(message.payload.decode("utf-8")))
    s = message.topic.split('/')[-1]
    val = float(str(message.payload.decode("utf-8")).split('=')[1])
    if s in data:
        data[s].append(val)
    else:
        data[s] = [val]
    #print(data)


client_id = 'c1'
broker_ip = 'broker.emqx.io'
broker_port = 1883

default_topic = 'mamei/sensors/#'

mqtt_client = mqtt.Client(f'mamei-{client_id}')
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect
print('connect',broker_ip, broker_port)
mqtt_client.connect(broker_ip, broker_port, keepalive=600)

mqtt_client.loop_start()

app = Flask(__name__)

@app.route('/sensors/<s>',methods=['POST'])
def add_data(s):
    val = request.values['val']
    if s in data:
        data[s].append(val)
    else:
        data[s] = [val]
    print(data)
    return 'ok',200

@app.route('/sensors/<s>',methods=['GET'])
def get_data(s):
    if s in data:
        return json.dumps(data[s]),200
    else:
        return 'sensor not found',404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


mqtt_client.loop_stop()