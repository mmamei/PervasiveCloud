#


import datetime
import ssl
import time
import jwt
import paho.mqtt.client as mqtt


# [START iot_mqtt_jwt]
def create_jwt(project_id, private_key_file, algorithm):
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
        Args:
         project_id: The cloud project ID this device belongs to
         private_key_file: A path to a file containing either an RSA256 or
                 ES256 private key.
         algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'
        Returns:
            A JWT generated from the given project_id and private key, which
            expires in 20 minutes. After 20 minutes, your client will be
            disconnected, and a new JWT will have to be generated.
        Raises:
            ValueError: If the private_key_file does not contain a known key.
        """

    token = {
        # The time that the token was issued at
        "iat": datetime.datetime.utcnow(),
        # The time the token expires.
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=20),
        # The audience field should always be set to the GCP project id.
        "aud": project_id,
    }

    # Read the private key file.
    with open(private_key_file, "r") as f:
        private_key = f.read()

    print(
        "Creating JWT using {} from private key file {}".format(
            algorithm, private_key_file
        )
    )

    return jwt.encode(token, private_key, algorithm=algorithm)



def on_message(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    payload = str(message.payload.decode("utf-8"))
    print(
        "Received message '{}' on topic '{}' with Qos {}".format(
            payload, message.topic, str(message.qos)
        )
    )
def on_publish(unused_client, unused_userdata, unused_mid):
    """Paho callback when a message is sent to the broker."""
    print("on_publish")

def get_client(
    project_id,
    cloud_region,
    registry_id,
    device_id,
    private_key_file,
    algorithm,
    ca_certs,
    mqtt_bridge_hostname,
    mqtt_bridge_port,
):
    """Create our MQTT client.

    The client_id is a unique string that identifies this device.
    For Google Cloud IoT Core, it must be in the format below.
    """
    client_id = "projects/{}/locations/{}/registries/{}/devices/{}".format(
        project_id, cloud_region, registry_id, device_id
    )
    print("Device client_id is '{}'".format(client_id))

    client = mqtt.Client(client_id=client_id)

    # With Google Cloud IoT Core, the username field is ignored, and the
    # password field is used to transmit a JWT to authorize the device.
    client.username_pw_set(
        username="unused", password=create_jwt(project_id, private_key_file, algorithm)
    )

    # Enable SSL/TLS support.
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    # Register message callbacks. https://eclipse.org/paho/clients/python/docs/
    # describes additional callbacks that Paho supports. In this example, the
    # callbacks just print to standard out.
    client.on_message = on_message
    client.on_publish = on_publish

    # Connect to the Google MQTT bridge.
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    # This is the topic that the device will receive configuration updates on.
    mqtt_config_topic = "/devices/{}/config".format(device_id)

    # Subscribe to the config topic.
    client.subscribe(mqtt_config_topic, qos=1)

    # The topic that the device will receive commands on.
    mqtt_command_topic = "/devices/{}/commands/#".format(device_id)

    # Subscribe to the commands topic, QoS 1 enables message acknowledgement.
    print("Subscribing to {}".format(mqtt_command_topic))
    client.subscribe(mqtt_command_topic, qos=0)

    return client


# [END iot_mqtt_config]



def mqtt_device_demo(args):
    """Connects a device, sends data, and receives data."""

    mqtt_topic = "/devices/{}/{}".format(args['device_id'], args['sub_topic'])

    jwt_iat = datetime.datetime.utcnow()
    jwt_exp_mins = args['jwt_expires_minutes']
    client = get_client(
        args['project_id'],
        args['cloud_region'],
        args['registry_id'],
        args['device_id'],
        args['private_key_file'],
        args['algorithm'],
        args['ca_certs'],
        args['mqtt_bridge_hostname'],
        args['mqtt_bridge_port'],
    )

    # Publish num_messages messages to the MQTT bridge once per second.
    for i in range(1, args['num_messages'] + 1):
        # Process network events.
        client.loop()

        payload = "{}/{}-payload-{}".format(args['registry_id'], args['device_id'], i)
        print("Publishing message {}/{}: '{}'".format(i, args['num_messages'], payload))
        try:
            client.publish(mqtt_topic, payload, qos=1)
        except Exception as e:
            print(e)
        time.sleep(1)

if __name__ == "__main__":
    args = {
        'project_id':'iot-mamei1',
        'cloud_region':'europe-west1',
        'registry_id':'mameireg',
        'mqtt_bridge_hostname':'mqtt.googleapis.com',
        'mqtt_bridge_port':8883,
        'device_id':'sensor1',
        'private_key_file':'rsa_private.pem',
        'num_messages':25,
        'sub_topic':'events',
        'algorithm':'RS256',
        'ca_certs':'roots.pem',
        'jwt_expires_minutes':20
    }
    mqtt_device_demo(args)
    print('end')
