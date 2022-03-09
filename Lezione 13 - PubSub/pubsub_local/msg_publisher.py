from google.cloud import pubsub_v1

project_id = 'pubsub-mamei'
topic_name = 'test-topic'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)

try:
    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Created topic: {topic.name}")
except Exception as e:
    print(e)


r = publisher.publish(topic_path,b'message 1',key1='val1',key2='val2')
print(r.result())
