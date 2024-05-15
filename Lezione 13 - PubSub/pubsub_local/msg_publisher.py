from google.cloud import pubsub_v1
from secret import project_id
from google.auth import jwt
import json
from topic_subscription_creator import create_topic
import time

service_account_info = json.load(open("credentials.json"))
audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
credentials = jwt.Credentials.from_service_account_info(service_account_info, audience=audience)
publisher = pubsub_v1.PublisherClient(credentials=credentials)

topic_path = create_topic('test123')

for i in range(10):
    r = publisher.publish(topic_path,b'message 1',key1=f'val{i}',key2='val2')
    print(r.result())
    time.sleep(5)
