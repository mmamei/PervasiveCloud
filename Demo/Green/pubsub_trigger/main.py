

def save_telemetry(event, context):
    import base64
    import json
    from google.cloud import bigquery
    print(f'This Function was triggered by messageId {context.event_id} published at {context.timestamp} to {context.resource["name"]}')
    if 'data' in event:
        payload = base64.b64decode(event['data']).decode('utf-8')
        data = json.loads(payload)
        project_id = 'iot-mamei1'
        dataset_id = 'dataset1'
        table_id = 'green1'
        #client = bigquery.Client.from_service_account_json('credentials2.json')
        client = bigquery.Client()
        rows_to_insert = [data]
        table_full_id = f'{project_id}.{dataset_id}.{table_id}'
        errors = client.insert_rows_json(table_full_id, rows_to_insert)  # Make an API request.
        if errors == []:
            print("New rows have been added.")
        else:
            print("Encountered errors while inserting rows: {}".format(errors))


