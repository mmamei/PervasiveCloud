import cv2
import zmq
import base64
import numpy as np
from video_config import *
import json
import time

# import msgpack

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
address = f'tcp://{broker_ip}:{broker_port_sub}'
print(address)
footage_socket.connect(address)

footage_socket.setsockopt_string(zmq.SUBSCRIBE, default_topic)
latencies_post = []
payload_size = []

experiment_start = 0
experiment_end = 0

while True:
    try:
        msg = footage_socket.recv_multipart()

        if experiment_start == 0:
            experiment_start = time.time()

        topic = msg[0].decode("utf-8")
        timestamp = float(msg[1].decode("utf-8"))
        image = msg[2]
        # print("Received Topic: %s" % topic)
        # print("Received Image: %s" % image)
        npimg = np.frombuffer(image, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        experiment_end = time.time()
        latencies_post.append((time.time() - timestamp) * 1000)
        payload_size.append((len(image) / (1024))*8)
        cv2.imshow("Stream", source)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break

print('----- STATS -----')
experiment_duration = (experiment_end - experiment_start)
print('Experiment Duration (s) = ', experiment_duration)
print('FPS Average (fps) = ', np.count_nonzero(payload_size)/experiment_duration)
print('Payload Size AVG (KBytes) =', np.mean(payload_size)/1024)
print('Payload Size AVG (KBits) =', np.mean(payload_size))
print('Message Rate AVG (MBits/Sec) =', ((np.sum(payload_size)/1024)/experiment_duration))
print('Delay Mean =', np.mean(latencies_post))
print('Delay Median =', np.median(latencies_post))
print('Delay SD =', np.std(latencies_post))
