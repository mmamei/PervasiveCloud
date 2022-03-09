from google.cloud import pubsub_v1

project_id = 'pubsub-mamei'
topic_name = 'test-topic'
subscription_name = 'pullsub'

subscriber = pubsub_v1.SubscriberClient()

subscription_path = subscriber.subscription_path(project_id,subscription_name)
print(subscription_path)
topic_path = subscriber.topic_path(project_id, topic_name)
print(topic_path)

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