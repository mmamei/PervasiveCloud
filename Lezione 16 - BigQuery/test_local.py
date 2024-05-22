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

    schema = [
        bigquery.SchemaField("sensor", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("lat", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("lon", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("value", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("datetime", "DATETIME", mode="REQUIRED"),
    ]

    table = bigquery.Table(table_full_id, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print(f'Created table {table.project}.{table.dataset_id}.{table.table_id}')

def insert(project_id,dataset_id,table_id):
    client = bigquery.Client.from_service_account_json('credentials.json')
    table_full_id = f'{project_id}.{dataset_id}.{table_id}'

    rows_to_insert = [
    {'sensor':'sensor1','value':3.4,'datetime':'2021-11-17 15:32:00'}, # DATETIME	A string in the form "YYYY-MM-DD [HH:MM:SS]"
    {'sensor':'sensor1','value':3.5,'datetime':'2021-11-17 15:33:00'},
    ]

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


def query(project_id,db_id,table):
    query = f'SELECT * FROM {project_id}.{db_id}.{table} LIMIT 100'
    client = bigquery.Client.from_service_account_json('credentials.json')
    query_job = client.query(query)
    for row in query_job:
        #print(row)
        # Row values can be accessed by field name or index.
        print(f'name={row[0]} datetime={row["datetime"]}')



if __name__ == '__main__':
    project_id = 'plcoud2024'
    region = 'europe-west8'
    db_id = 'test2'
    table = 'table2'
    #create_dataset(project_id,db_id,region)
    #create_table(project_id,db_id,table)
    #insert3(project_id, db_id, table)
    query(project_id,db_id,table)