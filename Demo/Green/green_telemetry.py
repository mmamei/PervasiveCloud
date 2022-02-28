

from datetime import datetime,timedelta
import json
import ssl
import time
import jwt
import paho.mqtt.client as mqtt
import Freenove_DHT as DHT
import RPi.GPIO as GPIO
from ADCDevice import *
import board
from adafruit_seesaw.seesaw import Seesaw

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
        "iat": datetime.utcnow(),
        # The time the token expires.
        "exp": datetime.utcnow() + timedelta(minutes=20),
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

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + mqtt.connack_string(rc))

def on_message(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    payload = str(message.payload.decode("utf-8"))
    print(f"Received message '{payload}' on topic '{message.topic}' with Qos {message.qos}")
    if payload == 'water':
        print('water!')
        GPIO.output(waterPin, GPIO.HIGH)  # make ledPin output HIGH level to turn on led
        time.sleep(2)  # Wait for 2 second
        GPIO.output(waterPin, GPIO.LOW)

def on_publish(unused_client, unused_userdata, unused_mid):
    print("publish", flush=True)
    pass


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
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish

    # Connect to the Google MQTT bridge.
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    # This is the topic that the device will receive configuration updates on.
    mqtt_config_topic = "/devices/{}/config".format(device_id)
    # Subscribe to the config topic.
    print("Subscribing to {}".format(mqtt_config_topic))
    client.subscribe(mqtt_config_topic, qos=1)

    # The topic that the device will receive commands on.
    mqtt_command_topic = "/devices/{}/commands/#".format(device_id)
    # Subscribe to the commands topic, QoS 1 enables message acknowledgement.
    print("Subscribing to {}".format(mqtt_command_topic))
    client.subscribe(mqtt_command_topic, qos=1)


    return client


# [END iot_mqtt_config]
adc = ADCDevice()
def setupADC():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)


DHTPin = 17  # define the pin of DHT11 in BCM
dht = None
def setupDHT():
    global dht
    dht = DHT.DHT(DHTPin, GPIO.BCM)

ss = None
def setupSeesaw():
    global ss
    i2c_bus = board.I2C()
    ss = Seesaw(i2c_bus, addr=0x36)

waterPin = 23 # define the pin of Water in BCM
def setupWater():
    # GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
    GPIO.setup(waterPin, GPIO.OUT)  # set the ledPin to OUTPUT mode
    GPIO.output(waterPin, GPIO.LOW)  # make ledPin output LOW level


def send_telemetry(args):
    """Connects a device, sends data, and receives data."""

    for i in range(0, 10):
        chk = dht.readDHT11()  # read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
        if (chk is dht.DHTLIB_OK):  # read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            #print("DHT11,OK!")
            break
        time.sleep(0.1)
    #print("Humidity : %.2f, \t Temperature : %.2f \n" % (dht.humidity, dht.temperature))


    value = adc.analogRead(0)  # read the ADC value of channel 0
    light = value / 255.0 * 3.3  # calculate the voltage value

    moist = ss.moisture_read()


    x = {
        'time':str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        'temp':dht.temperature,
        'humidity':dht.humidity,
        'light':light,
        'moisture':moist
    }

    payload = json.dumps(x)


    try:
        client.publish(mqtt_topic, payload, qos=1)
        print(payload, flush=True)
    except Exception as e:
        print('-------------------')
        print(e)


if __name__ == "__main__":
    args = {
        'project_id':'iot-mamei1',
        'cloud_region':'europe-west1',
        'registry_id':'mameireg',
        'mqtt_bridge_hostname':'mqtt.googleapis.com',
        'mqtt_bridge_port':8883,
        'device_id':'sensor1',
        'private_key_file':'rsa_private.pem',
        'sub_topic':'events',
        'algorithm':'RS256',
        'ca_certs':'roots.pem'
    }

    mqtt_topic = "/devices/{}/{}".format(args['device_id'], args['sub_topic'])


    setupWater()
    setupDHT()
    setupADC()
    setupSeesaw()

    last_send = 0

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


    try:
        while True:
            client.loop()
            now = time.time()
            if now - last_send > 60:
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
                send_telemetry(args)
                last_send = now
            time.sleep(1)
    except:
        print('exiting...')
    finally:
        GPIO.cleanup()
        adc.close()
