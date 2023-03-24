from requests import get, post
import time
import paho.mqtt.client as mqtt

# config http
base_url = 'http://localhost:80'
# config mqtt
broker_ip = 'broker.emqx.io'
broker_port = 1883

sensor = 's2'
http_flag = False
mqtt_flag = True
if mqtt_flag:
    mqtt_client = mqtt.Client(f'mamei-{sensor}')
    mqtt_client.connect(broker_ip, broker_port)
    mqtt_client.loop_start()

for i in range(1000):
    print(sensor,'invio....')
    if http_flag:
        r = post(f'{base_url}/sensors/{sensor}',data={'val': i})
    if mqtt_flag:
        infot = mqtt_client.publish(f'mamei/sensors/{sensor}',f'val={i}' )
        infot.wait_for_publish()
        print('Message Sent')

    time.sleep(5)

if mqtt_flag:
    mqtt_client.loop_stop()

print('done')
