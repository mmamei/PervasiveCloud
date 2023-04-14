from google.cloud import iot_v1, pubsub_v1
import io


def create_registry(
    service_account_json, project_id, cloud_region, pubsub_topic, registry_id
):
    """Creates a registry and returns the result. Returns an empty result if
    the registry already exists."""
    # [START iot_create_registry]
    # project_id = 'YOUR_PROJECT_ID'
    # cloud_region = 'us-central1'
    # pubsub_topic = 'your-pubsub-topic'
    # registry_id = 'your-registry-id'
    #client = iot_v1.DeviceManagerClient()
    client = iot_v1.DeviceManagerClient.from_service_account_json(service_account_json)
    parent = f"projects/{project_id}/locations/{cloud_region}"

    if not pubsub_topic.startswith("projects/"):
        pubsub_topic = "projects/{}/topics/{}".format(project_id, pubsub_topic)

    body = {
        "event_notification_configs": [{"pubsub_topic_name": pubsub_topic}],
        "id": registry_id,
    }
    try:
        response = client.create_device_registry(request={"parent": parent, "device_registry": body})
        print("Created registry")
        return response
    except Exception as e:
        print("Error, registry not created")
        print(e)


def create_topic(service_account_json,project_id,topic_id):
    publisher = pubsub_v1.PublisherClient.from_service_account_json(service_account_json)
    topic_path = publisher.topic_path(project_id, topic_id)
    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Created topic: {topic.name}")


def create_device(service_account_json, project_id, cloud_region, registry_id,device_id,certificate_file):
    # project_id = 'YOUR_PROJECT_ID'
    # cloud_region = 'us-central1'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # certificate_file = 'path/to/certificate.pem'

    client = iot_v1.DeviceManagerClient.from_service_account_json(service_account_json)

    parent = client.registry_path(project_id, cloud_region, registry_id)

    with io.open(certificate_file) as f:
        certificate = f.read()

    # Note: You can have multiple credentials associated with a device.
    device_template = {
        "id": device_id,
        "credentials": [
            {
                "public_key": {
                    "format": iot_v1.PublicKeyFormat.RSA_X509_PEM,
                    "key": certificate,
                }
            }
        ],
    }
    print('Created Device',device_id)
    return client.create_device(request={"parent": parent, "device": device_template})



if __name__ == '__main__':
    service_account_json='credentials2.json'
    project_id='iot-mamei1'
    cloud_region='europe-west1'
    pubsub_topic='telem1'
    registry_id='mameireg'

    #create_registry(service_account_json, project_id, cloud_region, pubsub_topic, registry_id)

    create_topic(service_account_json, project_id, pubsub_topic)

    device_id = 'sensor2'
    certificate_file = 'rsa_cert.pem'  # pem file
    #create_device(service_account_json, project_id, cloud_region, registry_id,device_id,certificate_file)