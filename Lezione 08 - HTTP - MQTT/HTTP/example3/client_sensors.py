from requests import get, post
import time

base_url = 'http://localhost:80'
sensor = 's1'
with open('CleanData_PM10.csv') as f:
    for l in f.readlines()[1:]:
        data,val = l.strip().split(',')
        print(data,val)
        r = post(f'{base_url}/sensors/{sensor}',
                 data={'data':data,'val':val})
        time.sleep(5)


print('done')
