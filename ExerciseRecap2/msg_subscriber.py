from google.cloud import pubsub_v1
from secret import project_id,topic_name
from google.auth import jwt
import numpy as np
import cv2 as cv
import base64
import json
import time
from google.cloud import storage

service_account_info = json.load(open("credentials.json"))
audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"
credentials = jwt.Credentials.from_service_account_info(
    service_account_info, audience=audience
)
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

service_account_info = json.load(open("credentials.json"))
audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
credentials = jwt.Credentials.from_service_account_info(
    service_account_info, audience=audience
)
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = subscriber.topic_path(project_id, topic_name)
'''
try:
    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Created topic: {topic.name}")
except Exception as e:
    print(e)
'''
subscription_name = 'pubsub2'
subscription_path = subscriber.subscription_path(project_id,subscription_name)
print(subscription_path)
# create subscription
'''
try:
    subscriber.create_subscription(name=subscription_path, topic=topic_path)
except Exception as e:
    print(e)
'''

img = np.zeros((240, 320, 3), np.uint8)

client = storage.Client.from_service_account_json('credentials.json')
bucket = client.get_bucket('video-mamei-test2')

def callback(msg):
    #print(f'messaggio ricevuto: {msg}')
    dict = json.loads(msg.data.decode('utf-8'))  # deserializzazione
    #print(dict, flush=True)
    x = base64.b64decode(dict['image'].encode('utf-8'))
    # converting into numpy array from buffer
    npimg = np.frombuffer(x, dtype=np.uint8)
    img = cv.imdecode(npimg, 1)
    name = str(int(time.time()))
    cv.imwrite('test.jpg', img)

    # bucket = client.bucket('upload-mamei-1')
    source_file_name = 'test.jpg'
    destination_blob_name = f'{name}.jpg'
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    #blob.upload_from_string(img)
    print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))
    msg.ack()

streaming_pull = subscriber.subscribe(subscription_path,callback=callback)

streaming_pull.result()
