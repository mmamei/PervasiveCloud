from google.cloud import bigquery
import pandas as pd

if __name__ == '__main__':
    project_id = 'mamei-test2-382313'
    region = 'europe-west1'
    db_id = 'test1'
    table = 'table2'
    query = f'SELECT * FROM {project_id}.{db_id}.{table} LIMIT 100'
    client = bigquery.Client.from_service_account_json('credentials.json')
    df = client.query(query).to_dataframe()
    print(df)