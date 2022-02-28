import cv2
import zmq
import base64
import numpy as np
from video_config import *
import json
import time
import msgpack
context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
address = f'tcp://{broker_ip}:{broker_port_sub}'
print(address)
footage_socket.connect(address)

footage_socket.setsockopt_string(zmq.SUBSCRIBE, default_topic)
latencies_post = []
while True:
    try:
        topic,message = footage_socket.recv_string().split('-')
        dict = json.loads(message)
        img = base64.b64decode(dict['image'].encode('utf-8'))
        npimg = np.frombuffer(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        latencies_post.append((time.time() - dict['time']) * 1000)
        cv2.imshow("Stream", source)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break

print('POST')
print('Mean =',np.mean(latencies_post))
print('Median =',np.median(latencies_post))
print('SD =' ,np.std(latencies_post))