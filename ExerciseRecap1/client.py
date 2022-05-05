#
from secret import secret
from requests import get, post
import time
base_url = 'https://testlez11.appspot.com'
with open('CleanData_PM10.csv') as f:
    for r in f:
        r = r.strip()
        t,pm10 = r.split(',')
        pm10 = float(pm10)
        r = post(f'{base_url}/sensors/sensor1', data={'time': t, 'pm10': pm10, 'secret':secret})
        print('sending',t,pm10)
        time.sleep(30)
