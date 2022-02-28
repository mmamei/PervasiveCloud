from google.cloud import bigquery
from datetime import datetime, timedelta
import random

def create_dataset(project_id,dataset_id,location):
    # Construct a BigQuery client object.
    client = bigquery.Client.from_service_account_json('credentials.json')
    dataset_full_id = f'{project_id}.{dataset_id}'
    dataset = bigquery.Dataset(dataset_full_id)
    dataset.location = location
    # Send the dataset to the API for creation, with an explicit timeout.
    # Raises google.api_core.exceptions.Conflict if the Dataset already
    # exists within the project.
    dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

def create_table(project_id,dataset_id,table_id):
    client = bigquery.Client.from_service_account_json('credentials.json')
    table_full_id = f'{project_id}.{dataset_id}.{table_id}'
    # {"time": "2022-02-24 18:44:32", "temp": 22.7, "humidity": 36, "light": 0.5435294117647058, "moisture": 100}
    schema = [
        bigquery.SchemaField("time", "DATETIME", mode="REQUIRED"),
        bigquery.SchemaField("temp", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("humidity", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("light", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("moisture", "FLOAT64", mode="REQUIRED"),
    ]

    table = bigquery.Table(table_full_id, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print(f'Created table {table.project}.{table.dataset_id}.{table.table_id}')

def insert(project_id,dataset_id,table_id):
    client = bigquery.Client.from_service_account_json('credentials.json')
    rows_to_insert = [
    {'sensor':'sensor1','value':3.4,'datetime':'2021-11-17 15:32:00'}, # DATETIME	A string in the form "YYYY-MM-DD [HH:MM:SS]"
    {'sensor':'sensor1','value':3.5,'datetime':'2021-11-17 15:33:00'},
    ]
    table_full_id = f'{project_id}.{dataset_id}.{table_id}'
    errors = client.insert_rows_json(table_full_id, rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

def insert2(project_id,dataset_id,table_id):
    client = bigquery.Client.from_service_account_json('credentials.json')
    table_full_id = f'{project_id}.{dataset_id}.{table_id}'

    dt = datetime.strptime('2021-11-17 15:33:00', '%Y-%m-%d %H:%M:%S')  # YYYY-MM-DD [HH:MM:SS]
    for i in range(100):
        dt += timedelta(minutes=1)
        #print(dt.strftime('%Y-%m-%d %H:%M:%S'))
        v = 3.4 + i + random.gauss(0,2)
        rows = [{'sensor': 'sensor1', 'value': v, 'datetime': dt.strftime('%Y-%m-%d %H:%M:%S')}]
        errors = client.insert_rows_json(table_full_id, rows)  # Make an API request.
        if errors == []:
            print("New rows have been added.")
        else:
            print("Encountered errors while inserting rows: {}".format(errors))

def insert3(project_id,dataset_id,table_id):
    client = bigquery.Client.from_service_account_json('credentials.json')
    table_full_id = f'{project_id}.{dataset_id}.{table_id}'

    dt = datetime.strptime('2021-11-17 17:33:00', '%Y-%m-%d %H:%M:%S')  # YYYY-MM-DD [HH:MM:SS]

    sensors = [
        {'id': 'modena','lat':44.64661935128612, 'lon':10.925714194043392},
        {'id': 'reggio emilia', 'lat': 44.69833568636162, 'lon': 10.63119575772369},
        {'id': 'mantova', 'lat': 45.158563488324816, 'lon': 10.793287903622467}
    ]

    for i in range(100):
        dt += timedelta(minutes=1)
        for s in sensors:
            v = 60 -  0.5*i + random.gauss(0,2)
            if i == 50:
                v += 100


            rows = [{'sensor': s['id'], 'lat': s['lat'], 'lon': s['lon'], 'value': v, 'datetime': dt.strftime('%Y-%m-%d %H:%M:%S')}]
            errors = client.insert_rows_json(table_full_id, rows)  # Make an API request.
            if errors == []:
                print("New rows have been added.")
            else:
                print("Encountered errors while inserting rows: {}".format(errors))



if __name__ == '__main__':
    #create_dataset('iot-mamei1','dataset1','europe-west1')
    create_table('iot-mamei1','dataset1','green1')
    #insert3('iot-mamei', 'test1', 'table2')
