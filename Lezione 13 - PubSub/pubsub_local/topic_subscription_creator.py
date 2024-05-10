
from google.cloud import pubsub_v1
from secret import project_id
from google.auth import jwt
import json



def create_topic(topic_name):
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

    return topic_path



def create_subscription(subscription_name, topic_name):
    service_account_info = json.load(open("credentials.json"))
    audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"
    credentials = jwt.Credentials.from_service_account_info(
        service_account_info, audience=audience
    )
    subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    topic_path = create_topic(topic_name)
    try:
        subscriber.create_subscription(name=subscription_path, topic=topic_path)
    except Exception as e:
        print(e)
    return subscription_path


if __name__ == '__main__':
    create_topic()