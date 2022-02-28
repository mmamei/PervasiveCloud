import json
from google.cloud import bigquery

payload = '{"time": "2022-02-24 18:44:32", "temp": 22.7, "humidity": 36, "light": 0.5435294117647058, "moisture": 100}'
data = json.loads(payload)
project_id = 'iot-mamei1'
dataset_id = 'dataset1'
table_id = 'green1'
client = bigquery.Client.from_service_account_json('credentials.json')
rows_to_insert = [data]
table_full_id = f'{project_id}.{dataset_id}.{table_id}'
errors = client.insert_rows_json(table_full_id, rows_to_insert)  # Make an API request.
if errors == []:
    print("New rows have been added.")
else:
    print("Encountered errors while inserting rows: {}".format(errors))