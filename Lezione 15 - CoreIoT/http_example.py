
import datetime
import jwt
from requests import post
import base64

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

#curl -X POST -H 'authorization: Bearer JWT' -H 'content-type: application/json' --data '{"binary_data": "DATA"}' -H 'cache-control: no-cache'
if __name__ == '__main__':
    project_id = 'iot-mamei'
    cloud_region = 'europe-west1'
    private_key_file = 'rsa_private.pem'
    algorithm = 'RS256'
    registry_id = 'mameireg4'
    device_id = 'device4'
    t = create_jwt(project_id,private_key_file,algorithm)
    headers = {'authorization': 'Bearer '+t}
    url = f'https://cloudiotdevice.googleapis.com/v1/projects/{project_id}/locations/{cloud_region}/registries/{registry_id}/devices/{device_id}:publishEvent'
    print(url)
    r = post(url, headers=headers, data={'binary_data': base64.b64encode(b'test')})
    print(r.status_code)
    print(r.text)
