from google.cloud import pubsub_v1
from secret import project_id,topic_name
from google.auth import jwt
subscription_name = 'pullsub'
import  json

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


subscription_path = subscriber.subscription_path(project_id,subscription_name)
print(subscription_path)
topic_path = subscriber.topic_path(project_id, topic_name)

try:
    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Created topic: {topic.name}")
except Exception as e:
    print(e)


# create subscription
try:
    subscriber.create_subscription(name=subscription_path, topic=topic_path)
except Exception as e:
    print(e)

def callback(msg):
    print(f'messaggio ricevuto: {msg}')
    msg.ack()

streaming_pull = subscriber.subscribe(subscription_path,callback=callback)

streaming_pull.result()

#try:
#    streaming_pull.result(timeout=10)
#except Exception as e:
#    print(e)
#    streaming_pull.cancel()