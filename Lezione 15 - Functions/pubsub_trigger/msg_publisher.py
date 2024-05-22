from google.cloud import pubsub_v1
from secret import project_id,topic_name
from google.auth import jwt
import json

service_account_info = json.load(open("credentials.json"))
audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
credentials = jwt.Credentials.from_service_account_info(service_account_info, audience=audience)
publisher = pubsub_v1.PublisherClient(credentials=credentials)

topic_path = publisher.topic_path(project_id, topic_name)
try:
    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Created topic: {topic.name}")
except Exception as e:
    print(e)


r = publisher.publish(topic_path,b'message 15567',key1='val1',key2='val2')
print(r.result())
