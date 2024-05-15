from google.cloud import pubsub_v1
from secret import project_id
from google.auth import jwt
import  json
from topic_subscription_creator import create_subscription

service_account_info = json.load(open("credentials.json"))
audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"
credentials = jwt.Credentials.from_service_account_info(
    service_account_info, audience=audience
)
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
subscription_path = create_subscription('pubsub3','test123')

def callback(msg):
    print(f'messaggio ricevuto: {msg}')
    msg.ack()

streaming_pull = subscriber.subscribe(subscription_path,callback=callback)


print('start_reading')

streaming_pull.result()

print('end')

#try:
#    streaming_pull.result(timeout=10)
#except Exception as e:
#    print(e)
#    streaming_pull.cancel()