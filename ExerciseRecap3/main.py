
# cloud function
def save_data_2_bq(request):
    from google.cloud import bigquery
    from datetime import datetime, timedelta
    client = bigquery.Client()
    project_id = 'mamei-test2-382313'
    dataset_id = 'test1'
    table_id = 'tabes3'
    table_full_id = f'{project_id}.{dataset_id}.{table_id}'

    request_json = request.get_json(silent=True)
    if request_json:
        sensor = request_json['sensor']
        dt = request_json['dt']
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')  # YYYY-MM-DD [HH:MM:SS]
        val = request_json['val']

        rows = [{'sensor': sensor, 'val': val, 'datetime': dt.strftime('%Y-%m-%d %H:%M:%S')}]
        errors = client.insert_rows_json(table_full_id, rows)  # Make an API request.
        if errors == []:
            return "New rows have been added."
        else:
            return "Encountered errors while inserting rows: {}".format(errors)
