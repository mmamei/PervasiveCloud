from google.cloud import pubsub_v1
from secret import project_id,topic_name
from google.auth import jwt
import  json
import time

service_account_info = json.load(open("credentials.json"))
audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
credentials = jwt.Credentials.from_service_account_info(
    service_account_info, audience=audience
)
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(project_id, topic_name)

try:
    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Created topic: {topic.name}")
except Exception as e:
    print(e)

client_id = 'sensor3'
with open('CleanData_PM10.csv') as f:
    for r in f:
        r = r.strip()
        t,pm10 = r.split(',')
        pm10 = float(pm10)
        payload_string = json.dumps({'sensor':client_id,'time':t,'pm10':pm10})
        r = publisher.publish(topic_path,b'message 1',payload=payload_string)
        print('message sent',t)
        time.sleep(10)



