from google.cloud import iot_v1


project_id='iot-mamei1'
cloud_region='europe-west1'
registry_id='mameireg'
device_id = 'sensor1'


print("Sending command to device")
service_account_json='credentials2.json'
client = iot_v1.DeviceManagerClient.from_service_account_json(service_account_json)
device_path = str(f'projects/{project_id}/locations/{cloud_region}/registries/{registry_id}/devices/{device_id}')
print(device_path)
command = 'water'
data = command.encode("utf-8")

client.send_command_to_device(request={"name": device_path, "binary_data": data})