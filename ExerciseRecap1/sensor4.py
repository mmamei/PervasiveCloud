#
from secret import secret
from requests import get, post
import time
import json
function_url = 'https://europe-west1-testlez11.cloudfunctions.net/save_data'
with open('CleanData_PM10.csv') as f:
    for r in f:
        r = r.strip()
        t,pm10 = r.split(',')
        pm10 = float(pm10)
        r = post(function_url, data = {'data': json.dumps({'sensor':'sensor4','time': t, 'pm10': pm10, 'secret':secret})})
        print('sending',t,pm10,' -----> ',r.status_code)
        time.sleep(5)
