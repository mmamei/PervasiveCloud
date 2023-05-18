from requests import get, post
import time

base_url = 'https://europe-west1-mamei-test2-382313.cloudfunctions.net/save_data_2_bq'

sensor = 's2'

with open('CleanData_PM10.csv') as f:
    for l in f:
        dt,v = l.strip().split(',')
        v = float(v)
        # print({'sensor':'s1', 'dt': dt, 'val':v})
        r = post(f'{base_url}', json={'sensor':'s1', 'dt': dt, 'val':v})
        print(r.text)
        time.sleep(3)

print('done')
